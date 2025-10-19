import os
from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from .embeddings_port import EmbeddingsPort, l2_normalize

def _prep(t: str) -> str:
    return " ".join((t or "").strip().split())

class SpanishHFEmbeddings(EmbeddingsPort):
    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or os.getenv(
            "EMB_MODEL",
            "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )
        self.model = SentenceTransformer(self.model_name)

    def encode(self, texts: List[str]) -> np.ndarray:
        clean = [_prep(t) for t in texts]
        vecs = self.model.encode(clean, convert_to_numpy=True, show_progress_bar=False)
        return l2_normalize(vecs)
