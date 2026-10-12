"""Explicit startup factory used by examples, the API and manual evaluation."""

import json
from importlib.resources import files

from langchain_ollama import ChatOllama, OllamaEmbeddings

from text2sql.agent import SQLAgent
from text2sql.config import Settings
from text2sql.database import Database
from text2sql.retrieval import ExampleRetriever


def build_agent(settings: Settings) -> SQLAgent:
    database = Database(
        settings.database_url.get_secret_value(),
        max_rows=settings.max_rows,
        statement_timeout_ms=settings.statement_timeout_ms,
    )
    database.initialize()
    embeddings = OllamaEmbeddings(
        model=settings.embedding_model,
        base_url=settings.ollama_url,
        client_kwargs={"timeout": settings.model_timeout_seconds},
    )
    examples = json.loads(files("text2sql").joinpath("few_shots.json").read_text())
    retriever = (
        ExampleRetriever(examples, embeddings, k=settings.few_shot_k)
        if (settings.few_shot_k)
        else None
    )
    model = ChatOllama(
        model=settings.model,
        base_url=settings.ollama_url,
        temperature=0,
        reasoning=False,
        seed=42,
        num_ctx=8192,
        num_predict=1024,
        client_kwargs={"timeout": settings.model_timeout_seconds},
    )
    return SQLAgent(
        model=model,
        database=database,
        retriever=retriever,
        max_iterations=settings.max_iterations,
        max_tool_calls=settings.max_tool_calls,
    )
