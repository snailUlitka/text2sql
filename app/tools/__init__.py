"""Module stores tools for OllamaFunction based agent."""
from typing import List

from app.tools.base import AgentBaseTool
from app.tools.sql_query_tool import SQLQueryTool
from app.tools.db_table_info_tool import DatabaseTableInfoTool
from app.tools.db_table_list_tool import DatabaseTableListTool
from app.tools.sql_checker_tool import SQLCheckerTool

from langchain_community.utilities.sql_database import SQLDatabase
from langchain.chat_models.base import BaseChatModel


def get_tools(
    llm: BaseChatModel,
    db: SQLDatabase
) -> List[AgentBaseTool]:
    return [
        SQLQueryTool(db),
        DatabaseTableInfoTool(db),
        DatabaseTableListTool(db),
        SQLCheckerTool(llm, db)
    ]


__all__ = [
    "AgentBaseTool",
    "SQLQueryTool",
    "DatabaseTableInfoTool",
    "DatabaseTableListTool",
    "SQLCheckerTool"
]
