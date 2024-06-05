"""Tool for check SQL query."""
import re
from typing import (
    Dict,
    List,
    Optional,
    Any
)

from llm_app.tools.base import AgentBaseTool

from langchain.chat_models.base import BaseChatModel
from langchain.agents.openai_tools.base import convert_to_openai_tool
from langchain.prompts import (
    ChatPromptTemplate,
    BaseChatPromptTemplate
)

from langchain_core.messages.human import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.pydantic_v1 import (
    BaseModel,
    Field
)

from langchain_community.utilities.sql_database import SQLDatabase

KEY_WORDS = [
    "CONSTRAINT",
    "CHECK",
    "UNIQUE",
    "PRIMARY",
    "FOREIGN",
    "EXCLUDE",
    "DEFERRABLE",
    "NOT",
    "INITIALLY",
    "LIKE",
]

QUERY_CHECKER_PROMPT = """
Double check the {dialect} query for common mistakes, including:
- Using NOT IN with NULL values
- Using UNION when UNION ALL should have been used
- Using BETWEEN for exclusive ranges
- Data type mismatch in predicates
- Properly quoting identifiers
- Using the correct number of arguments for functions
- Casting to the correct data type
- Using the proper columns for joins

Also check that all column and table names correspond to the database, these \
are the ones you need to check:

{db_names}

If there are any of the above mistakes, rewrite the query. If there are no \
mistakes, just reproduce the original query.

OUTPUT THE FINAL SQL QUERY ONLY."""


class SQLCheckerTool(AgentBaseTool):
    def __init__(
        self,
        llm: BaseChatModel,
        db: SQLDatabase,
        *,
        tool_name="__query_sql_checker_tool",
        key_words: Optional[List[str]] = None,
        checker_prompt: Optional[BaseChatPromptTemplate] = None
    ):
        """
        `key_words` - keywords that are used in the 
        CREATE TABLE construction, `keywords` are excluded when parsing names
        """
        super().__init__(db, tool_name=tool_name)
        
        self.llm = llm
        self.key_words = key_words or KEY_WORDS

        if checker_prompt is None:
            self.checker_prompt = ChatPromptTemplate.from_messages((
                ("system", QUERY_CHECKER_PROMPT),
                ("human", "SQL Query: SELECT name FROM passenger;"),
                ("ai", "SELECT passenger_name FROM passenger;"),
                ("human", "SQL Query: SELECT plane FROM flight;"),
                ("ai", "SELECT plane FROM trip;"),
                ("human", "SQL Query: {query}")
            ))
        else:
            self.checker_prompt = checker_prompt

    class QuerySQLCheckerTool(BaseModel):
        """INPUT to this tool is a QUERY to check, 
        OUTPUT is a CORRECT QUERY in database. 
        Use this tool to double check if 
        your query is correct before executing it. 
        Always use this tool before executing a 
        query with '<query_tool>'!"""
        query_to_check: str = Field(
            description="SQL query that needs to be checked before execution."
        )

    def _exclude_key_words_from_list(
        self,
        list: List[str]
    ) -> List[str]:
        return [
            column_name_or_key_word
            for column_name_or_key_word in list
            if column_name_or_key_word.upper() not in self.key_words
        ]

    def _extract_names_from_db(self):
        # Removes VARCHAR(60) and others for subsequent processing
        clean_sql = re.sub(r"\(\d+\)", "", self.db.get_table_info())

        # Removes sample rows in table info
        clean_sql = re.sub(r"/\*(.|\s)*?\*/", "", clean_sql)

        # Get all table names
        table_names = re.findall(r"CREATE TABLE (\w+) \(", clean_sql)

        names = []

        for name in table_names:
            # Returns a description {names}
            table_sql = re.search(
                fr"CREATE TABLE {name} \((\s+(.|\s+)*?)\s+\)", clean_sql
            ).group(1)

            # Gets all column names and constraints (this is noise)
            columns_part = re.findall(r"\n\t(\w+)", table_sql)

            names.append({
                "name": name,
                # Exclude constraints (noise)
                "columns": self._exclude_key_words_from_list(columns_part)
            })

        return names

    def _execute_tool(self, **kwargs) -> str:
        query_to_check = kwargs.get("query_to_check")
        
        if not isinstance(query_to_check, str):
            raise ValueError("'kwargs' should contain 'query_to_check' and " +
                             "'query_to_check' should be 'str'") 
            
        db_names_list = self._extract_names_from_db()

        db_names = ""
        for name_pair in db_names_list:
            db_names += f"Table name: {name_pair["name"]}" +\
                f"\n\tColumn names: {name_pair["columns"]}\n"

        chain = (
            self.checker_prompt.partial(db_names=db_names)
            | self.llm
            | StrOutputParser()
        )
        return chain.invoke({
            "query": query_to_check,
            "dialect": self.db.dialect,
        })

    def get_function(self, **kwargs) -> Dict[str, Any]:
        query_tool_name = kwargs.get("query_tool_name", 
                                    "__query_sql_database_tool")
        
        func = convert_to_openai_tool(self.QuerySQLCheckerTool)["function"]

        func["name"] = self.tool_name

        func["description"] = re.sub(
            r"<query_tool>",
            query_tool_name,
            func["description"]
        )

        func["description"] = re.sub(r"\s+", " ", func["description"])

        return func

    def wrap_result_with_human_message(
        self, 
        tool_result: str,
        example=False, 
        **kwargs
    ):
        return HumanMessage(
            content="I can help you execute the tool. Give me a second... " +
            "And so, I think I managed to call it, but I can't read " +
            "what's written there, only a smart AI can understand it." +
            "\nI checked, the result of the tool\n" +
            "It looks like an SQL query! I think it's the " +
            "right one. Try to execute this query." +
            "\n\nResult of tool: \n" + tool_result,
            example=example
        )
