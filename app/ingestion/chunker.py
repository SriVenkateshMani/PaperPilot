from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.logger import get_logger

logger = get_logger(__name__)

def text_chunk(sections):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 150
    )

    chunks = []

    skip_sections = {
        "references",
        "bibliography",
        "authors",
        "author",
        "affiliations",
        "acknowledgments",
        "acknowledgements",
        "content"
    }

    for section in sections:
        title = section["title"]
        content = section["content"].strip()

        if title.strip().lower() in skip_sections:
            continue

        if not content:
            continue

        section_chunks = splitter.split_text(content)

        for chunk in section_chunks:
            chunks.append(f"Section: {title}\n\n{chunk}")

    return chunks