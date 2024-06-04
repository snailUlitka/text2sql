"""Tool for execute SQL query"""
import re
from typing import (
    Dict,
    Any
)

from app.tools.base import AgentBaseTool

from langchain.agents.openai_tools.base import convert_to_openai_tool

from langchain_core.messages.human import HumanMessage
from langchain_core.pydantic_v1 import (
    BaseModel,
    Field
)

from langchain_community.utilities.sql_database import SQLDatabase


class SQLQueryTool(AgentBaseTool):
    def __init__(
        self,
        db: SQLDatabase,
        *,
        tool_name="__query_sql_database_tool"
    ):
        super().__init__(db, tool_name=tool_name)

    class QuerySQLDatabaseTool(BaseModel):
        """INPUT to this tool is a DETAILED and CORRECT SQL query, 
        OUTPUT is a RESULT FROM the DATABASE. If the query is not 
        correct, an error message will be returned. If an error is 
        returned, rewrite the query, check the query, and try again. 
        If you encounter an issue with Unknown column 'xxxx' in 
        'field list', use '<info_tool>' to query 
        the correct table fields."""
        sql_query: str = Field(
            description="Detailed and correct SQL query."
        )

    def _execute_tool(self, **kwargs):
        sql_query = kwargs.get("sql_query")
        
        if not isinstance(sql_query, str):
            raise ValueError("'kwargs' should contain 'sql_query' and " +
                             "'sql_query' should be 'str'") 
        
        result: Dict[str, str] = {}

        try:
            result["type"] = "ok"
            result["result"] = self.db.run(sql_query)
        except Exception as e:
            result["type"] = "error"
            result["result"] = str(e)

        return result

    def get_function(self, **kwargs) -> Dict[str, Any]:
        info_tool_name = kwargs.get("info_tool_name", 
                                    "__info_sql_database_tool")
        
        func = convert_to_openai_tool(self.QuerySQLDatabaseTool)["function"]

        func["name"] = self.tool_name

        func["description"] = re.sub(
            r"<info_tool>",
            info_tool_name,
            func["description"]
        )

        func["description"] = re.sub(r"\s+", " ", func["description"])

        return func

    def get_tool(self):
        return self._execute_tool

    def wrap_result_with_human_message(
        self,
        tool_result: Dict[str, str],
        example=False,
        **kwargs
    ):
        conversational_tool_name = kwargs.get(
            "conversational_tool_name", 
            "__conversational_response"
        )
        
        info_tool_name = kwargs.get(
            "info_tool_name",
            "__info_sql_database_tool"
        )
        
        if tool_result["type"] == "ok":
            human_message = "This is similar to the database " +\
                "response. Maybe there's something I need there. " +\
                "I can't see it, please help me understand, if " +\
                "there is an response to my question, please give it " +\
                f"to me, use it for this: '{conversational_tool_name}'"
        elif tool_result["type"] == "error":
            human_message = "Oops.. There seems to be a mistake here. " +\
                "Apparently the request was incorrect, try to fix it! " +\
                f"Use '{info_tool_name}' to get info about database" +\
                "\nREWRITE QUERY AND COME BACK WITH RESPONSE!"
                
        return HumanMessage(
            content="I can help you execute the tool. Give me a second... " +
            "And so, I think I managed to call it, but I can't read " +
            "what's written there, only a smart AI can understand it." +
            f"\nI checked, the result of the tool\n{human_message}" +
            "\n\nResult of tool: \n" + tool_result["result"],
            example=example
        )
