"""
Provides access to the vector database according to the specified parameters `local_data.py` data for connection.
Data in `local_data.py` you can create using `local_data_template.py`
"""
from langchain_community.vectorstores.pgvector import PGVector
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
from local_data import (
    PASSWORD_OF_VC_STORE,
    VC_USER,
    VC_NAME,
    VC_PORT
)


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


def get_selector(embedding_llm, examples: list[dict[str, str]]) -> SemanticSimilarityExampleSelector:
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
        k=3,
        connection_string=CONNECTION_STRING,
        pre_delete_collection=True,
        use_jsonb=True
    )

    return example_selector


if __name__ == "__main__":
    from langchain_community.embeddings.ollama import OllamaEmbeddings
    llama_embeddings = OllamaEmbeddings(
        model="llama2:13b", temperature=0.25, repeat_penalty=1
    )

    examples = [{"input": "Print all airlines",
                 "query": "SELECT * FROM company;"}]

    print(get_selector(llama_embeddings, examples)
          .select_examples({"imput": "SELECT * FROM passenger"})
          )
