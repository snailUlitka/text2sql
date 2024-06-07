"""Agent to interact with SQL database based on OllamaFunctions wrapper"""
from typing import (
    List,
    Tuple,
    Dict,
    Optional
)

from llm_app.tools import get_tools
from llm_app.tools import AgentBaseTool
from llm_app.prompts import PromptGenerator

from langchain_core.runnables import (
    RunnableLambda, 
    Runnable
)
from langchain.schema.agent import (
    AgentFinish, 
    AgentActionMessageLog
)
from langchain.chat_models.base import BaseChatModel
# TODO:_DEPRECATED____________________________________________
from langchain.agents.output_parsers.openai_functions import (
    OpenAIFunctionsAgentOutputParser
)

from langchain_community.utilities.sql_database import SQLDatabase

from langchain_core.messages.ai import AIMessage
from langchain_core.runnables import RunnablePassthrough

from langchain_experimental.llms.ollama_functions import (
    OllamaFunctions,
    DEFAULT_RESPONSE_FUNCTION
)


class OllamaFunctionsSQLAgent:
    def __init__(
        self,
        *,
        ollama_functions: OllamaFunctions,
        chat_llm: BaseChatModel,
        prompt_generator: PromptGenerator,
        db: SQLDatabase,
        extra_tools: Optional[List[AgentBaseTool]] = None,
        iteration_limit=10
    ):
        self.ollama_functions = ollama_functions
        self.chat_llm = chat_llm
        self.prompt_generator = prompt_generator
        self.db = db
        self.tools = get_tools(chat_llm, db)

        if extra_tools is not None:
            self.tools + extra_tools

        self.iteration_limit = iteration_limit

    def format_to_ollama_chat_messages(
        self,
        intermediate_steps: List[
            Tuple[
                AgentActionMessageLog,
                str | Dict[str, str]
            ]
        ]
    ):
        agent_scratchpad = []

        for step in intermediate_steps:
            agent_scratchpad.append(
                AIMessage(
                    content="{ " +
                    f"'tool': '{step[0].tool}', " +
                    f"'tool_input': {step[0].tool_input}"
                )
            )

            tool_result = None

            for tool in self.tools:
                if tool.get_tool_name() == step[0].tool:
                    tool_result = tool.wrap_result_with_human_message(step[1])
                    break

            if tool_result is None:
                raise ToolNotFoundException(step[0].tool)

            agent_scratchpad.append(
                tool_result
            )

        return agent_scratchpad

    def _intermediate_steps_to_agent_scratchpad(self, steps):
        return self.format_to_ollama_chat_messages(steps['intermediate_steps'])

    def _get_agent(self):
        llm_with_tools = self.ollama_functions.bind_tools(
            tools=[t.get_function() for t in self.tools] +
            [DEFAULT_RESPONSE_FUNCTION]
        )

        agent = (
            RunnablePassthrough.assign(
                agent_scratchpad=self._intermediate_steps_to_agent_scratchpad
            )
            | self.prompt_generator.get_prompt(db=self.db, llm=self.chat_llm)
            | llm_with_tools
            | OpenAIFunctionsAgentOutputParser()
        )

        return agent
    
    # TODO: Edit signature for all run funcs
    # TODO: REFACTOR THIS
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def run_agent(
        self,
        input: str,
        top_k: int
    ) -> AgentFinish | str:
        number_of_iteration = 0
        intermediate_steps = []

        while number_of_iteration < self.iteration_limit:
            result = self._get_agent().invoke({
                "dialect": self.db.dialect,
                "input": input,
                "top_k": top_k,
                "intermediate_steps": intermediate_steps
            })
            # TODO: ADD LOGGING
            if isinstance(result, AgentFinish):
                return result
            else:
                result: AgentActionMessageLog = result

            tool_to_execute = None

            for tool in self.tools:
                if tool.get_tool_name() == result.tool:
                    tool_to_execute = tool
                    break

            if tool_to_execute is None:
                raise ToolNotFoundException(result.tool)

            if isinstance(result.tool_input, str):
                observation = tool(result.tool_input)
            else:
                observation = tool_to_execute.get_tool()(**result.tool_input)
            intermediate_steps.append((result, observation))
            number_of_iteration += 1

        return "Agent stop due to limited number of iterations!"
    
    async def async_run_agent(
        self,
        input: str,
        top_k: int
    ) -> AgentFinish | str:
        number_of_iteration = 0
        intermediate_steps = []

        while number_of_iteration < self.iteration_limit:
            result = await self._get_agent().ainvoke({
                "dialect": self.db.dialect,
                "input": input,
                "top_k": top_k,
                "intermediate_steps": intermediate_steps
            })

            if isinstance(result, AgentFinish):
                return result
            else:
                result: AgentActionMessageLog = result

            tool_to_execute = None

            for tool in self.tools:
                if tool.get_tool_name() == result.tool:
                    tool_to_execute = tool
                    break

            if tool_to_execute is None:
                raise ToolNotFoundException(result.tool)

            if isinstance(result.tool_input, str):
                observation = tool(result.tool_input)
            else:
                observation = tool_to_execute.get_tool()(**result.tool_input)
            intermediate_steps.append((result, observation))
            number_of_iteration += 1

        return "Agent stop due to limited number of iterations!"
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _run_agent_wrapper(self, input_dict: Dict[str, str | int]):
        input = input_dict.get("input")
        top_k = input_dict.get("top_k", 20)

        return self.run_agent(input, top_k)
    
    def _async_run_agent_wrapper(self, input_dict: Dict[str, str | int]):
        input = input_dict.get("input")
        top_k = input_dict.get("top_k", 20)

        return self.async_run_agent(input, top_k)

    def get_runnable(self) -> Runnable:
        return RunnableLambda(func=self._run_agent_wrapper, 
                              afunc=self._async_run_agent_wrapper)


class ToolNotFoundException(Exception):
    def __init__(self, tool_name):
        self.tool_name = tool_name
        self.message = f"Tool with name '{self.tool_name}' was not found."
        super().__init__(self.message)
