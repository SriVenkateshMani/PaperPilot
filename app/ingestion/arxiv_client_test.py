from app.ingestion.arxiv_client import search_papers
from app.logger import get_logger

logger = get_logger(__name__)

papers = search_papers("retrieval augmented generation", 5)

for paper in papers:
    logger.info(f"Title, {paper.title}")
    logger.info(f"Author, {[author.name for author in paper.authors]}")
    logger.info(f"Arxiv ID:  {paper.entry_id}")