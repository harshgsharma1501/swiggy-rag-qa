from sentence_transformers import SentenceTransformer
import numpy as np
from utils.config import EMBEDDING_MODEL

class Embedder:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)

    def embed(self, texts):
        return np.array(
            self.model.encode(texts, normalize_embeddings=True)
        )