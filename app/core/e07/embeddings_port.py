from abc import ABC, abstractmethod
from typing import List
import numpy as np

class EmbeddingsPort(ABC):
    @abstractmethod
    def encode(self, texts: List[str]) -> np.ndarray:
        ...

def l2_normalize(x: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(x, axis=1, keepdims=True) + 1e-12
    return x / norms
