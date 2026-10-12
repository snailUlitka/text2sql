"""Small semantic example index in memory, constructed explicitly at startup."""

from langchain_core.embeddings import Embeddings
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.vectorstores import InMemoryVectorStore


class ExampleRetriever:
    def __init__(self, examples: list[dict[str, str]], embeddings: Embeddings, *, k: int = 3):
        if not examples or not 1 <= k <= len(examples):
            raise ValueError("Provide examples and a valid retrieval count.")
        self.selector = SemanticSimilarityExampleSelector.from_examples(
            examples, embeddings, InMemoryVectorStore, k=k, input_keys=["input"]
        )

    def select(self, question: str) -> list[dict[str, str]]:
        return self.selector.select_examples({"input": question})
