import math
import re
from collections import Counter
from app.schemas.recommendation_schemas import TextComplexityResponse


class TextComplexityEvaluator:
    """
    Simula una API de PNL para calcular la complejidad lingüística y temática de un texto.
    """

    def evaluate_text(self, text: str) -> TextComplexityResponse:
        # 1️⃣ Limpieza del texto
        clean_text = re.sub(r'[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s]', '', text)
        words = clean_text.split()
        sentences = re.split(r'[.!?]', text)

        # 2️⃣ Métricas básicas
        word_count = len(words)
        sentence_count = max(len([s for s in sentences if s.strip() != '']), 1)
        avg_sentence_length = word_count / sentence_count

        # 3️⃣ Longitud promedio de palabras
        avg_word_length = sum(len(w) for w in words) / max(word_count, 1)

        # 4️⃣ Vocabulario único
        unique_words = len(set(words))
        lexical_density = unique_words / max(word_count, 1)

        # 5️⃣ Cálculo del índice de complejidad (tipo Flesch adaptado)
        complexity_score = (
            0.4 * avg_sentence_length +
            0.6 * avg_word_length +
            20 * (1 - lexical_density)
        )

        # Normalizamos entre 0–100
        normalized_score = min(max(100 - complexity_score * 5, 0), 100)

        # 6️⃣ Clasificación cualitativa
        if normalized_score > 70:
            level = "Fácil"
        elif normalized_score > 40:
            level = "Moderado"
        else:
            level = "Difícil"

        # 7️⃣ Generamos respuesta
        return TextComplexityResponse(
            score=round(normalized_score, 2),
            level=level,
            metrics={
                "avg_sentence_length": round(avg_sentence_length, 2),
                "avg_word_length": round(avg_word_length, 2),
                "lexical_density": round(lexical_density, 2),
                "word_count": word_count,
                "sentence_count": sentence_count
            }
        )
