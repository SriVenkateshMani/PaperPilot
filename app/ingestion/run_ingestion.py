from app.ingestion.store_papers import ingest_papers
from app.ingestion.pdf_downloader import download_paper
from app.ingestion.pdf_parser import parse_pdf
from app.ingestion.indexer import create_index, index_chunks
from app.ingestion.embedder import embed_chunks
from app.ingestion.chunker import text_chunk

from app.logger import get_logger

logger = get_logger(__name__)

create_index()

papers = ingest_papers(
    'all:"retrieval augmented generation"', 
    5
    )

for paper in papers:
    file_path = download_paper(paper)

    text = parse_pdf(file_path)

    chunks = text_chunk(text)

    embeddings = embed_chunks(chunks)

    index_chunks(paper, embeddings, chunks)

    logger.info(f"Indexed {len(chunks)} chunks for {paper.title}")
