import arxiv

from app.logger import get_logger

logger = get_logger(__name__)

def search_papers(query, max_results = 5):
    logger.info("Searching arXiv for query: %s", query)

    # Build the arXiv search request
    search = arxiv.Search(
        query = query,
        max_results = max_results,
        sort_by = arxiv.SortCriterion.SubmittedDate
    )

    # Create a client that will actually communicate with arXiv
    client = arxiv.Client(
        page_size = max_results,
        delay_seconds = 3,
        num_retries = 3
    )

    # store the searched results as a list
    try:
        results = list(client.results(search))

        logger.info(f"Fetched {len(results)} papers from arXiv")

        return results

    except arxiv.HTTPError as e:
        logger.erro(f"arXiv API failed: {e}")
        return []