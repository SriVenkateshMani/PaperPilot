from app.ingestion.indexer import client, INDEX_NAME
from app.logger import get_logger

def bm25_search(query: str, k: int = 5):
    body = build_bm25_query(query, k)

    return client.search(
        index=INDEX_NAME,
        body=body
    )

    