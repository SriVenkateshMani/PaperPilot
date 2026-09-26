from app.logger import get_logger
from app.retrieve.hybrid_search import hybrid_search

logger = get_logger(__name__)

results = hybrid_search(
    "how does retrieval augmented generation work?",
    k=5
)

for i, hit in enumerate(results, start=1):
    logger.info(
        f"Rank {i} | "
        f"RRF: {hit['rrf_score']} | "
        f"Title: {hit['_source']['title']} | "
        f"Chunk: {hit['_source']['chunk_id']}"
    )   

    logger.info(hit["_source"]["text"])