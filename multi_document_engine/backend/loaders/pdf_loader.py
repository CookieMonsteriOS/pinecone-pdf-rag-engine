import pdfplumber
from pathlib import Path


def load_pdfs(pdf_dir: str):
    pdf_dir = Path(pdf_dir)
    documents = []

    for pdf_file in pdf_dir.glob("*.pdf"):
        with pdfplumber.open(pdf_file) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    documents.append({
                        "document": pdf_file.name,
                        "page": i + 1,
                        "text": text
                    })
    return documents
