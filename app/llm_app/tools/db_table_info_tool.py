"""Tool for getting info about listed tables"""
import re
from typing import (
    Dict,
    Any
)

from llm_app.tools.base import AgentBaseTool

from langchain_core.utils.function_calling import convert_to_openai_tool

from langchain_core.messages.human import HumanMessage
from langchain_core.pydantic_v1 import (
    BaseModel,
    Field
)

from langchain_community.utilities.sql_database import SQLDatabase


class DatabaseTableInfoTool(AgentBaseTool):
    def __init__(
        self,
        db: SQLDatabase,
        *,
        tool_name="__info_sql_database_tool"
    ):
        super().__init__(db, tool_name=tool_name)

    class InfoSQLDatabaseTool(BaseModel):
        """
        INPUT to this tool is a comma-separated LIST OF TABLES, 
        output is the schema and sample rows for those tables. 
        Be sure that the tables actually exist by calling 
        '<list_tool>' first! Example Input: table1, table2, table3.
        This tool will not help if you need to get information about a column!
        """
        list_of_tables: str = Field(
            description="Comma-separated list of tables. Example: table1, " +
                "table2, table3"
        )

    def _execute_tool(self, **kwargs):
        list_of_tables = kwargs.get("list_of_tables")
        
        if not isinstance(list_of_tables, str):
            raise ValueError("'kwargs' should contain 'list_of_tables' and " +
                             "'list_of_tables' should be 'str'")
        
        res = ""

        res += "company, " if "company" in list_of_tables else ""
        res += "pass_in_trip, " if "pass_in_trip" in list_of_tables else ""
        res += "passenger, " if "passenger" in list_of_tables else ""
        res += "trip, " if "trip" in list_of_tables else ""

        res = res[:-2]

        return self.db.get_table_info_no_throw(
            [t.strip() for t in res.split(",")]
        )

    def get_function(self, **kwargs) -> Dict[str, Any]:
        list_tool_name = kwargs.get("list_tool_name", 
                                    "__list_sql_database_tool")
        
        func = convert_to_openai_tool(self.InfoSQLDatabaseTool)["function"]

        func["name"] = self.tool_name
        
        func["description"] = re.sub(
            r"<list_tool>", 
            list_tool_name, 
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
                "It looks like the structure of the database " +
                "tables(s). Maybe this will help you write the right query? " +
                "Please make sure you remember the names!" +
                "\n\nResult of tool: \n" + tool_result,
                example=example
        )
