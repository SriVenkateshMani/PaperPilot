from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.logger import get_logger

logger = get_logger(__name__)

def text_chunk(text: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        overlap = 150
    )

    chunks = splitter.split_text(text)

    logger.info(f"Created {len(chunk)} chunks")

    return chunks