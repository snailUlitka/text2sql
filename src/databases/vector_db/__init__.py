"""Vector database to store embeddings"""
from src.databases.vector_db.vc_connect import (
    get_selector,
    get_vc
)

__all__ = [
    "get_selector",
    "get_vc"
]
