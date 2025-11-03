import math
import re
from collections import Counter
from app.schemas.recommendation_schemas import TextComplexityResponse
from app.models.resultado_texto import ResultadoTexto
from app.models.texto  import Texto
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.models.resultado_juego import ResultadoJuego

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

# Calcula promedio de registro en la tabla resultado_texto, segun un usuario y un juego
def obtener_promedio_dificultad_por_usuario_y_juego(db: Session, id_usuario: int, id_juego: int):
    stmt = (
        select(func.avg(Texto.id_dificultad).label("promedio_dificultad"))
        .select_from(ResultadoTexto)
        .join(Texto, ResultadoTexto.id_texto == Texto.id_texto)
        .join(ResultadoJuego, ResultadoTexto.id_juego == ResultadoJuego.id_juego)
        .where(
            ResultadoTexto.id_usuario == id_usuario,
            ResultadoTexto.id_juego == id_juego
        )
    )

    resultado = db.execute(stmt).scalar()  # obtiene un solo valor (el promedio)

    if resultado is not None:
        return {"id_usuario": id_usuario, "id_juego": id_juego, "promedio_dificultad": round(resultado,2),"promedio_dificultad_entero":int(round(resultado))}
    
    return {"detail": "No se encontraron textos para este usuario y juego."}


# Calcular si el resultado es positivo del juego (15 preguntas)
def obtener_resultado_general_juego(db: Session, id_usuario: int, id_juego: int):
    stmt = (
        select(ResultadoJuego.correctas.label("correctas"),
               ResultadoJuego.incorrectas.label("incorrectas"),
               (ResultadoJuego.correctas - ResultadoJuego.incorrectas).label("resol"))
        .select_from (ResultadoJuego)
        .where(
            ResultadoJuego.id_usuario == id_usuario,
            ResultadoJuego.id_juego == id_juego
        )
    )
    resultado = db.execute(stmt).first()
    if resultado is None:
        return {"detail": "No se encontraron resultados para este usuario y juego."}

    # Calcular resultado del juego
    resol = resultado.resol or -1
    resultado_juego = 1 if resol > 0 else 0

    return {
        "id_usuario": id_usuario,
        "id_juego": id_juego,
        "correctas": resultado.correctas,
        "incorrectas": resultado.incorrectas,
        "resultado_juego": resultado_juego
    }
