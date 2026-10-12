from langchain_core.embeddings import Embeddings

from text2sql.retrieval import ExampleRetriever


class EmbeddingsStub(Embeddings):
    def embed_documents(self, texts):
        return [[1.0, 0.0] if "passenger" in text else [0.0, 1.0] for text in texts]

    def embed_query(self, text):
        return [1.0, 0.0]


def test_semantic_selector_returns_example_metadata():
    retriever = ExampleRetriever(
        [
            {"id": "names", "input": "List passenger names", "query": "SELECT passenger_name"},
            {"id": "companies", "input": "List companies", "query": "SELECT company_name"},
        ],
        EmbeddingsStub(),
        k=1,
    )
    selected = retriever.select("Who is travelling?")
    assert selected == [
        {"id": "names", "input": "List passenger names", "query": "SELECT passenger_name"}
    ]
