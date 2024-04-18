from examples import FEW_SHOT_EXAMPLES

from langchain_community.vectorstores.pgvector import PGVector
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector


def get_vc(embedding_llm) -> PGVector:
    from local_data import (
        PASSWORD_OF_VC_STORE,
        VC_USER,
        VC_NAME,
        VC_PORT
    )

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


def get_selector(embedding_llm) -> SemanticSimilarityExampleSelector:
    from local_data import (
        PASSWORD_OF_VC_STORE,
        VC_USER,
        VC_NAME,
        VC_PORT
    )

    CONNECTION_STRING = PGVector.connection_string_from_db_params(
        driver="psycopg2",
        host="localhost",
        port=VC_PORT,
        database=VC_NAME,
        user=VC_USER,
        password=PASSWORD_OF_VC_STORE
    )

    example_selector = SemanticSimilarityExampleSelector.from_examples(
        FEW_SHOT_EXAMPLES,
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

    print(get_selector(llama_embeddings)
          .select_examples({"imput": "SELECT * FROM passenger"})
          )
