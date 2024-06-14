"""Tool for getting a list of tables"""
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


class DatabaseTableListTool(AgentBaseTool):
    def __init__(
        self,
        db: SQLDatabase,
        *,
        tool_name="__list_sql_database_tool"
    ):
        super().__init__(db, tool_name=tool_name)

    class ListSQLDatabaseTool(BaseModel):
        """INPUT to this tool is a EMPTY STRING, 
        OUTPUT is a comma-separated LIST OF TABLES 
        in database. Use this tool to select the 
        tables needed to respond to the user."""
        empty_string: str = Field(description="Empty string")

    def _execute_tool(self, **kwargs):
        return ", ".join(self.db.get_usable_table_names())

    def get_function(self, **kwargs) -> Dict[str, Any]:
        func = convert_to_openai_tool(self.ListSQLDatabaseTool)["function"]

        func["name"] = self.tool_name
        func["description"] = re.sub(r"\s+", " ", func["description"])

        return func

    def wrap_result_with_human_message(
        self,
        tool_result: str,
        example=False,
        **kwagrs
    ):
        info_tool_name = kwagrs.get("info_tool_name", 
                                    "__info_sql_database_tool")
        
        return HumanMessage(
            content="I can help you execute the tool. Give me a second... " +
            "And so, I think I managed to call it, but I can't read " +
            "what's written there, only a smart AI can understand it." +
            "\nI checked, the result of the tool\n" +
            "It looks like a list of table names. " +
            "Maybe it will help to get an response. I think if you don't " +
            f"have enough information, you can use this: '{info_tool_name}'" +
            "\n\nResult of tool: \n" + tool_result,
            example=example
        )
