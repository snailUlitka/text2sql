"""Base tool for OllamaFunction based agent"""
from typing import (
    Dict,
    Any
)
from abc import (
    ABC,
    abstractmethod
)

from langchain_community.utilities.sql_database import SQLDatabase

from langchain_core.messages.human import HumanMessage


class AgentBaseTool(ABC):
    def __init__(
        self,
        db: SQLDatabase,
        *,
        tool_name="__base_tool_name"
    ):
        self.db = db
        self.tool_name = tool_name

    def get_tool_name(self):
        return self.tool_name

    def get_tool(self):
        return self._execute_tool
    
    @abstractmethod
    def _execute_tool(self, **kwargs) -> str | Dict[str, str]:
        pass

    @abstractmethod
    def get_function(self, **kwargs) -> Dict[str, Any]:
        pass

    @abstractmethod
    def wrap_result_with_human_message(
        self,
        tool_result: str | Dict[str, str],
        example: bool,
        **kwargs
    ) -> HumanMessage:
        pass

    @abstractmethod
    def get_function(self, **kwargs) -> Dict[str, Any]:
        pass
