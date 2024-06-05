"""Root package of llm langchain app"""
from typing import Optional

from llm_app.databases.external_db import get_db
from llm_app.prompts import PromptGenerator
from llm_app.examples import FEW_SHOT_EXAMPLES

from llm_app.agents import OllamaFunctionsSQLAgent

from langchain.embeddings.base import Embeddings
from langchain.chat_models.base import BaseChatModel
from langchain_community.chat_models.ollama import ChatOllama
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_experimental.llms.ollama_functions import OllamaFunctions


def get_ollamafunctions_agent(
    *,
    chat_llm: Optional[BaseChatModel] = None,
    ollama_functions: Optional[OllamaFunctions] = None,
    embedding_llm: Optional[Embeddings] = None,
    db: Optional[SQLDatabase] = None,
    prompt_generator: Optional[PromptGenerator] = None
) -> OllamaFunctionsSQLAgent:
    """
    Create and retrieve an instance of OllamaFunctionsSQLAgent.
    
    This function initializes and returns an `OllamaFunctionsSQLAgent` by 
        setting up the required components:
    - `chat_llm`: A language model customized for dialogue.
    - `ollama_functions`: Functions leveraging the Ollama language model.
    - `embedding_llm`: A language model for creating embeddings.
    - `db`: A SQL database for storing and retrieving data.
    - `prompt_generator`: A generator for creating prompts with few-shot 
        examples.
    
    Each component has a default setup if not provided:
    - `chat_llm` uses the 'llama3:instruct' model with a temperature of 0.
    - `ollama_functions` also uses the 'llama3:instruct' model with a JSON 
        format and a temperature of 0.
    - `embedding_llm` uses the 'llama3:instruct' model with a temperature of 0.
    - `db` is retrieved using `get_db()`.
    - `prompt_generator` utilizes `PromptGenerator` configured with 
        `FEW_SHOT_EXAMPLES` and `embedding_llm`.
    
    Parameters:
    - chat_llm (Optional[BaseChatModel]): The chat language model to be used.
    - ollama_functions (Optional[OllamaFunctions]): Functions leveraging the 
        Ollama language model.
    - embedding_llm (Optional[Embeddings]): The language model for generating 
        embeddings.
    - db (Optional[SQLDatabase]): The SQL database instance.
    - prompt_generator (Optional[PromptGenerator]): The prompt generator 
        instance.
    
    Returns:
    - OllamaFunctionsSQLAgent: An instance of OllamaFunctionsSQLAgent 
        configured with the specified or default components.
    """

    chat_llm = chat_llm or ChatOllama(model="llama3:instruct",
                                      temperature=0)

    ollama_functions = ollama_functions or OllamaFunctions(
        model="llama3:instruct",
        format="json",
        temperature=0
    )

    embedding_llm = embedding_llm or OllamaEmbeddings(model="llama3:instruct",
                                                      temperature=0)

    db = db or get_db()

    prompt_generator = prompt_generator or \
        PromptGenerator().set_example_selector(
            examples=FEW_SHOT_EXAMPLES,
            embedding_llm=embedding_llm,
        )

    return OllamaFunctionsSQLAgent(
        ollama_functions=ollama_functions,
        chat_llm=chat_llm,
        prompt_generator=prompt_generator,
        db=db
    )
