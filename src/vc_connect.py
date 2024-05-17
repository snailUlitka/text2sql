"""
Provides access to the vector database according to the specified parameters `local_data.py` data for connection.
Data in `local_data.py` you can create using `local_data_template.py`
"""

from typing import (
    Dict,
    List
)

from local_data import (
    PASSWORD_OF_VC_STORE,
    VC_USER,
    VC_NAME,
    VC_PORT
)

from langchain_community.vectorstores.pgvector import PGVector

from langchain.prompts.example_selector import SemanticSimilarityExampleSelector


from langchain.embeddings.base import Embeddings


def get_vc(embedding_llm) -> PGVector:
    CONNECTION_STRING = PGVector.connection_string_from_db_params(
        driver="psycopg2",
        host="localhost",
        port=VC_PORT,
        database=VC_NAME,
        user=VC_USER,
        password=PASSWORD_OF_VC_STORE
    )

    db = PGVector(CONNECTION_STRING, embedding_llm,
                  pre_delete_collection=True, use_jsonb=True
                  )

    return db


def get_selector(
    *,
    embedding_llm: Embeddings,
    examples: list[dict[str, str]],
    k=3,
    input_keys 
) -> SemanticSimilarityExampleSelector:
    CONNECTION_STRING = PGVector.connection_string_from_db_params(
        driver="psycopg2",
        host="localhost",
        port=VC_PORT,
        database=VC_NAME,
        user=VC_USER,
        password=PASSWORD_OF_VC_STORE
    )

    example_selector = SemanticSimilarityExampleSelector.from_examples(
        examples,
        embedding_llm,
        PGVector,
        k=k,
        input_keys=input_keys,
        connection_string=CONNECTION_STRING,
        pre_delete_collection=True,
        use_jsonb=True
    )

    return example_selector
