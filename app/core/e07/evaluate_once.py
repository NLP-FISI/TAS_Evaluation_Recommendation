import os
from typing import List, Dict
import numpy as np
from .hf_embeddings import SpanishHFEmbeddings
from .error_repr import build_error_text

def _cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    return float((a @ b) / ((np.linalg.norm(a)+1e-12)*(np.linalg.norm(b)+1e-12)))

class FeedbackEmbeddingEvaluator:
    def __init__(self, threshold: float | None = None):
        self.model = SpanishHFEmbeddings()
        self.threshold = threshold if threshold is not None else float(os.getenv("EMB_SIM_THRESHOLD", "0.29"))

    def evaluate(self, mensaje_texto: str, tipo_error: str, grado: int, pistas: List[str]) -> Dict:
        err_text = build_error_text(tipo_error, grado, pistas)
        v_msg, v_err = self.model.encode([mensaje_texto, err_text])
        sim = _cosine_sim(v_msg, v_err)
        return {
            "similaridad_error": sim,
            "ok": sim >= self.threshold,
            "razones": {"tipo_error": tipo_error, "grado": grado, "pistas": pistas}
        }
