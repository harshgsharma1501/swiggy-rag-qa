import fitz
from utils.config import PDF_PATH

def load_pdf():
    doc = fitz.open(PDF_PATH)
    pages = []

    for i in range(len(doc)):
        page = doc[i]
        text = page.get_text("text")

        pages.append({
            "text": text,
            "page_number": i + 1
        })

    return pages