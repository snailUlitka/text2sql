"""
Module stores `PromptGenerator` which 
generate prompt from pieces like `PREFIX`, `SUFFIX`, etc.
"""

from typing import (
    Optional,
    List,
    Dict
)

from llm_app.databases.vector_db import get_selector
from llm_app.databases.external_db import get_db
from llm_app.examples.messages_examples import get_messages_example
from llm_app.prompts.sql_expert_prompt import (
    PREFIX,
    TABLE_DESCRIPTIONS,
    SUFFIX,
)

from langchain.embeddings.base import Embeddings
from langchain.chat_models.base import BaseChatModel

from langchain_core.example_selectors import BaseExampleSelector

from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    SystemMessagePromptTemplate,
)

from langchain_community.utilities.sql_database import SQLDatabase


class PromptGenerator:
    def __init__(self):
        self.example_selector = None
        self.prompt = None

    def set_example_selector(
        self,
        *,
        examples: Optional[List[Dict[str, str]]],
        k = 3,
        embedding_llm: Optional[Embeddings] = None,
        example_selector: Optional[BaseExampleSelector] = None,
        input_keys: List[str] = ["input"]
    ):
        if not examples:
            raise ValueError(
                "List of 'examples' should contain 1 or more items")

        if embedding_llm is None and example_selector is None:
            raise ValueError(
                "Must provide exactly one of 'embedding_llm' or " +
                    "'example_selector'. Received neither."
            )
        if embedding_llm and example_selector:
            raise ValueError(
                "Must provide exactly one of 'embedding_llm' or " +
                    "'example_selector'. Received both."
            )

        if example_selector:
            self.example_selector = example_selector
        else:
            self.example_selector = get_selector(
                embedding_llm=embedding_llm,
                examples=examples,
                k=k,
                input_keys=input_keys
            )

        return self

    def get_prompt(
        self,
        *,
        db: SQLDatabase,
        llm: BaseChatModel,
        prefix: str = None,
        suffix: str = None,
        table_names: List[str] = None,
        table_descriptions: Dict[str, str] = None,
        example_prompt: Optional[PromptTemplate] = None,
        input_variables: List[str] = ["dialect", "input", "top_k"]
    ) -> ChatPromptTemplate:
        """Generate prompt with few-shots example selector.

        Args:
            prefix - `"f-string"` or plain `str`
            suffix - `"f-string"` or plain `str`
            table_names - `List[str]`: List of table names.
            table_descriptions - `Dict[str, str]`: For example 
            {"name_of_table": "description"}, all names from the `table_names` 
            list should be listed.
            example_prompt - `PromptTemplate`: Default or if `None` 
            "User input: {input} SQL query: {query}".
            input_variables - `List[str]`: List of variables in `prefix` and 
            `suffix`. Defaults to [`"dialect"`, `"input"`, `"top_k"`, 
            `"table_names"`, `"table_descriptions"`].
        """
        if self.example_selector is None:
            raise ValueError(
                "'example_selector' is not specified. Before calling, " +
                    "use the method: 'set_example_selector'"
            )

        if not (prefix and suffix and table_names and table_descriptions):
            prefix = PREFIX
            suffix = SUFFIX
            table_names = get_db().get_usable_table_names()
            table_descriptions = TABLE_DESCRIPTIONS

        if not all(key in table_descriptions for key in table_names):
            raise ValueError(
                "All names from the `table_names` list should be listed in " +
                    "'table_descriptions' keys."
            )

        if example_prompt is None:
            example_prompt = PromptTemplate.from_template(
                "User input: {input}\nSQL query: {query}"
            )

        few_shots_prompt = FewShotPromptTemplate(
            prefix=prefix,
            suffix=suffix,
            example_selector=self.example_selector,
            example_prompt=example_prompt,
            input_variables=input_variables
        )
        
        messages = [SystemMessagePromptTemplate(prompt=few_shots_prompt)]
        messages += get_messages_example(db, llm)
        messages += [
            (
                "human",
                "Well, thanks! Help me with another question now. {input}"
            ),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ]

        self.prompt = ChatPromptTemplate.from_messages(messages)

        table_descriptions = "\n\n".join([
            f"{name}: {description}" for (name, description)
            in table_descriptions.items() if name in table_names
        ])
        table_names = ", ".join(table_names)

        self.prompt = self.prompt.partial(
            table_names=table_names,
            table_descriptions=table_descriptions,
            agent_scratchpad=[]
        )

        return self.prompt
