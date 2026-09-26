""" 
PDF is in binary format 
Convert to text
"""

from docling.document_converter import DocumentConverter
from app.logger import get_logger

logger = get_logger(__name__)

def parse_pdf(file_path):
    converter = DocumentConverter()

    # Convert the PDF into a structured Docling document
    result = converter.convert(file_path)
    logger.info(type(result))

    # Structure Document object into markdown text
    text = result.document.export_to_markdown()

    logger.info(f"Extracted {len(text)} characters from PDF")

    return text