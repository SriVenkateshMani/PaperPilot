from app.retrieve.bm25_search import bm25_search
from app.retrieve.semantic_search import semantic_search

def hybrid_search(query: str, k: int = 5):
    # Perform BM25 search
    bm25_results = bm25_search(query, k)

    # Perform semantic search
    semantic_results = semantic_search(query, k)

    return semantic_results, bm25_results