from app.ingestion.indexer import client, INDEX_NAME
from app.logger import get_logger

# The way to talk to the index is to use a match query
def build_bm25_query(query: str, k: int):
    return {
        "size": k,
        "query": {
            "match": {
                "text": query
            }
        }
    }

# Actually perform the BM25 search using the Elasticsearch client
def bm25_search(query: str, k: int = 5):
    body = build_bm25_query(query, k)

    return client.search(
        index=INDEX_NAME,
        body=body
    )

