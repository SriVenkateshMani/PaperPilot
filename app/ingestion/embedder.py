from sentence_transformers import SentenceTransformer
from app.logger import get_logger

logger = get_logger(__name__)

model = SentenceTransformer("all-MiniLm-L6-v2")

def embed_chunks(chunks: list[str]):
    logger.info(f"Generating embeddings for {len(chunks)} chunks")

    embeddings = model.encode(
        chunks,
        normalize_embeddings = True
    )

# Returns a list of vectors