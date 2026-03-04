import pickle
from dotenv import load_dotenv
import os

from embeddings.embedder import Embedder
from rag.retriever import retrieve
from rag.generator import generate_answer

# Load environment variables
load_dotenv()

print("Loading vector store...")
with open("vector_store.pkl", "rb") as f:
    vector_store = pickle.load(f)

embedder = Embedder()

while True:
    query = input("\nAsk a question (or type 'exit'): ")

    if query.lower() == "exit":
        break

    print("\nRetrieving relevant context...")
    chunks = retrieve(query, embedder, vector_store)

    print(f"Retrieved {len(chunks)} chunks")

    answer = generate_answer(chunks, query)

    print("\nFinal Answer:")
    print(answer)

    if chunks:
        print("\nSupporting Context:")
        for c in chunks:
            print(f"\nPage {c['metadata']['page_number']} | Score: {round(c['score'],3)}")
            print(c["text"][:400])
            print("-" * 60)