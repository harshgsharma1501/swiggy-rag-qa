from ingestion.financial_parser import parse_financial_summary
from ingestion.pdf_loader import load_pdf
from ingestion.chunking import chunk_documents
from embeddings.embedder import Embedder
from embeddings.vector_store import VectorStore

import json
import pickle

print("Loading PDF...")
pages = load_pdf()

print("Extracting structured financial data...")

# Proper structured format
financial_data = {
    "standalone": {},
    "consolidated": {}
}

for page in pages:
    if page["page_number"] == 5:
        structured = parse_financial_summary(page["text"])
        financial_data["standalone"].update(structured)

    if page["page_number"] == 6:
        structured = parse_financial_summary(page["text"])
        financial_data["consolidated"].update(structured)

with open("financial_data.json", "w") as f:
    json.dump(financial_data, f, indent=4)

print("Structured financial data saved.")

print("Chunking...")
chunks = chunk_documents(pages)

texts = [c["text"] for c in chunks]
metadata = [c["metadata"] for c in chunks]

print("Generating embeddings...")
embedder = Embedder()
embeddings = embedder.embed(texts)

dimension = embeddings.shape[1]
vector_store = VectorStore(dimension)

vector_store.add(embeddings, texts, metadata)

with open("vector_store.pkl", "wb") as f:
    pickle.dump(vector_store, f)

print("Index built successfully.")