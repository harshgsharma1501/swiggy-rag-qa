from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.config import CHUNK_SIZE, CHUNK_OVERLAP

def chunk_documents(pages):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = []

    for page in pages:
        splits = splitter.split_text(page["text"])

        for chunk in splits:
            chunks.append({
                "text": chunk,
                "metadata": {
                    "page_number": page["page_number"]
                }
            })

    return chunks