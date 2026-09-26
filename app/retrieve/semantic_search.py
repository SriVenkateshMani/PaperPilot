from app.ingestion.embedder import model
from app.ingestion.indexer import client, INDEX_NAME
from app.logger import get_logger

def semantic_search(query: str, k: int = 5):
    # Using the same model as in embed_chunks to ensure consistency
    query_embedding = model.encode(
        query,
        normalize_embeddings=True
    )

    # Build the ANN query return with the top k results
    body = build_knn_query(
        query_embedding.tolist(),
        k
    )

    # return the search results from the ANN index
    return client.search(
        index=INDEX_NAME,
        body=body
    )