""" 
PDF is in binary format 
Convert to text
"""

from docling.document_converter import DocumentConverter
from app.logger import get_logger

logger = get_logger(__name__)


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


def parse_pdf(file_path):
    converter = DocumentConverter()

    # Convert the PDF into a structured Docling document
    result = converter.convert(file_path)
    logger.info(type(result))

    # Structure Document object into markdown text
    text = result.document.export_to_maarkdown()

    logger.info(f"Extracted {len(text)} characters from PDF")



    for element in doc.texts[:5]:
        logger.info(f"Element type: {type(element)}")
        logger.info(f"Label: {element.label}")
        logger.info(f"Text: {element.text[:200]}")