import math

def prob_correct(theta, beta):
    return 1.0 / (1.0 + math.exp(-(theta - beta)))

def actualizar_dificultad(theta, racha, beta, resultado, eta=0.6): 
    """
    theta: dificultad acumulada actual (float)
    racha: entero entre -3 y +3 (valor previo)
    beta: dificultad del reto anterior (1..5)
    resultado: 1 si correcto, 0 si incorrecto
    devuelve: theta_nuevo, racha_nuevo, beta_siguiente, prob_estimada
    """
    p = prob_correct(theta, beta)
    
    # actualizar racha
    if resultado == 1:
        racha = min(racha + 1, 3)
    else:
        racha = max(racha - 1, -3)
    
    # factor por racha
    factor = 1.0 + 0.1 * abs(racha)
    
    # actualizar theta
    theta_nuevo = theta + eta * factor * (resultado - p)
    
    # limitar theta_nuevo entre 1 y 5
    theta_nuevo = max(1, min(5, theta_nuevo))
    
    # mapear a dificultad siguiente
    beta_siguiente = round(theta_nuevo)
    
    return theta_nuevo, racha, beta_siguiente, p


# #DATOS>
# theta = 3.0   # dificultad acumulada inicial
# racha = 0     # sin racha aún
# beta = 3      # el reto anterior fue dificultad 3


# resultados = [1, 1, 1, 1, 0, 0]  # tres aciertos seguidos

# for r in resultados:
#     theta, racha, beta_siguiente, p = actualizar_dificultad(theta, racha, beta, r)
#     print(f"r={r}, θ={theta:.3f}, racha={racha}, prob={p:.3f}, siguiente={beta_siguiente}")
#     beta = beta_siguiente
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
