""" 
PDF is in binary format 
Convert to text
"""

from docling.document_converter import DocumentConverter
from app.logger import get_logger

logger = get_logger(__name__)


# Extract sections from the Docling document based on titles and section headers
def extract_sections(doc):
    sections = []

    current_section = {
        "title": "Content",
        "content": ""
    }

    for element in doc.texts:

        if element.label in ["title", "section_header"]:

            if current_section["content"].strip():
                sections.append(current_section)

            current_section = {
                "title": element.text.strip(),
                "content": ""
            }

        elif element.text:
            current_section["content"] += element.text + "\n"

    if current_section["content"].strip():
        sections.append(current_section)

    return sections


# Parse the PDF file and extract text and structured sections (both cause the text is a fallback)
def parse_pdf(file_path):
    converter = DocumentConverter()

    # Convert the PDF into a structured Docling document
    result = converter.convert(file_path)
    logger.info(type(result))

    doc = result.document

    # Extract structured sections
    sections = extract_sections(doc)

    # Structure Document object into markdown text
    text = doc.export_to_markdown()

    logger.info(f"Extracted {len(text)} characters from PDF")

    return {
        "text": text,
        "sections": sections
    }