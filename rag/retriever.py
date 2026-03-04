from utils.config import TOP_K, SIMILARITY_THRESHOLD

def retrieve(query, embedder, vector_store):
    query_embedding = embedder.embed([query])[0]

    results = vector_store.search(query_embedding, TOP_K)

    SIMILARITY_THRESHOLD = 0.60

    filtered = [
        r for r in results
        if r["score"] >= SIMILARITY_THRESHOLD
    ]

    return filtered