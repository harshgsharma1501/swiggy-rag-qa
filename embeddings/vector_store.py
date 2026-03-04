import faiss
import numpy as np

class VectorStore:
    def __init__(self, dimension):
        self.index = faiss.IndexFlatIP(dimension)
        self.texts = []
        self.metadata = []

    def add(self, embeddings, texts, metadata):
        self.index.add(embeddings)
        self.texts.extend(texts)
        self.metadata.extend(metadata)

    def search(self, query_embedding, top_k):
        scores, indices = self.index.search(
            np.array([query_embedding]), top_k
        )

        results = []

        for score, idx in zip(scores[0], indices[0]):
            if idx != -1:
                results.append({
                    "text": self.texts[idx],
                    "metadata": self.metadata[idx],
                    "score": float(score)
                })

        return results