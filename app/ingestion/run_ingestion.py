from app.ingestion.store_papers import ingest_papers
from app.ingestion.pdf_downloader import download_paper
from app.ingestion.pdf_parser import parse_pdf
from app.ingestion.indexer import create_index
from app.ingestion.embedder import embed_chunks
from app.ingestion.chunker import text_chunk

from app.logger import get_logger

logger = get_logger(__name__)

create_index()

papers = ingest_papers("retrieval augmented generation", 5)

if papers:
    paper = papers[0]
    file_path = download_paper(papers[0])

    text = parse_pdf(file_path)

    chunks = text_chunk(text)

    embeddings = embed_chunks(chunks)

    index_chunks(paper, chunks, embeddings)

    logger.info(f"Indexed {len(chunks)} chunks")
