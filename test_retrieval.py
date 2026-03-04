import pickle
from embeddings.embedder import Embedder
from utils.config import TOP_K, SIMILARITY_THRESHOLD

print("Loading vector store...")
with open("vector_store.pkl", "rb") as f:
    vector_store = pickle.load(f)

embedder = Embedder()

query = "What was the net loss after tax in FY24?"

print("\nQuery:", query)

query_embedding = embedder.embed([query])[0]

results = vector_store.search(query_embedding, TOP_K)

print("\nTop retrieved chunks (no threshold):\n")

for r in results:
    print(f"Page: {r['metadata']['page_number']} | Score: {round(r['score'],3)}")
    print(r["text"][:300])
    print("-" * 60)

print(f"\nRetrieved {len(filtered)} relevant chunks:\n")

for r in filtered:
    print(f"Page: {r['metadata']['page_number']} | Score: {round(r['score'],3)}")
    print(r["text"][:400])
    print("-" * 60)