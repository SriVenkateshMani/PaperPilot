from app.database import SessionLocal
from app.ingestion.arxiv_client import search_papers
from app.models import Paper
from app.logger import get_logger

logger = get_logger(__name__)

# Save the retrieved content metadata from ARXIV to postgres
def ingest_papers(query: str, max_results: int = 5):
    with SessionLocal() as db:
        try:
            papers = search_papers(query, max_results)

            for result in papers:
                paper = Paper(
                    title = result.title,
                    author = ", ".join(author.name for author in result.authors)
                )
                db.add(paper)

            db.commit()

            logger.info(f"Stored {len(papers)} papers in the postgres")

        except Exception as e:
            db.rollback()
            logger.info(f"database error: {e}")