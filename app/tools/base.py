"""Base tool for OllamaFunction based agent"""
from typing import (
    Dict,
    Any
)
from types import FunctionType
from abc import (
    ABC,
    abstractmethod
)

from langchain_core.messages.human import HumanMessage


class AgentBaseTool(ABC):
    @abstractmethod
    def get_tool_name(self): pass

    @abstractmethod
    def wrap_result_with_human_message(
        self,
        tool_result: str | Dict[str, str],
        example,
        **kwargs
    ) -> HumanMessage:
        pass

    @abstractmethod
    def get_function(self) -> Dict[str, Any]: pass

    @abstractmethod
    def get_tool(self) -> FunctionType: pass