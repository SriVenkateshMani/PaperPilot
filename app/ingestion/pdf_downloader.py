from pathlib import Path
from app.logger import get_logger
from urllib.request import urlretrieve

logger = get_logger(__name__)

def download_paper(paper, download_dir: str = "data/arxiv_pdfs"):
    download_path = Path(download_dir)
    download_path.mkdir(parents = True, exist_ok = True)

    logger.info(f"Downloading paper: {paper.title}")

    # Extract the file name
    file_name = paper.pdf_url.split("/")[-1] + ".pdf"

    # Create the path where to store
    file_path = download_path / file_name

    # save the pdf from the url in the path
    urlretrieve(paper.pdf_url, file_path)

    logger.info(f"Downloaded PDF to: {file_path}")

    return file_path