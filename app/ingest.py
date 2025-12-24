# app/ingest.py

from pathlib import Path
from pypdf import PdfReader

def load_pdf(file_path: Path) -> str:
    """
    Extracts text from a PDF file.
    """
    reader = PdfReader(str(file_path))
    text = []

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text.append(page_text)

    return "\n".join(text)
