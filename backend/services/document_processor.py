from pathlib import Path
from pypdf import PdfReader
from docx import Document


def extract_pdf_text(file_path: str) -> str:
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text 

    return text


def extract_docx_text(file_path: str) -> str:
    document = Document(file_path)

    text = ""

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            text += paragraph.text

    return text


def extract_text(file_path: str) -> str:
    path = Path(file_path)

    if path.suffix.lower() == ".pdf":
        return extract_pdf_text(str(path))

    if path.suffix.lower() == ".docx":
        return extract_docx_text(str(path))

    raise ValueError("Unsupported file type")