from app.ingestion.store_papers import ingest_papers
from app.ingestion.pdf_downloader import download_paper
from app.ingestion.pdf_parser import parse_pdf
from app.logger import get_logger

logger = get_logger(__name__)
papers = ingest_papers("retrieval augmented generation", 5)

if papers:
    file_path = download_paper(papers[0])

    text = parse_pdf(file_path)

    logger.info(f"Parsed text length: {len(text)}")