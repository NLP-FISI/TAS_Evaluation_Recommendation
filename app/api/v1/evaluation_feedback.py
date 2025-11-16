from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.resultado_juego import ResultadoJuego

router = APIRouter()

@router.post("/feedback")
def generar_feedback(id_resultado_juego: int, db: Session = Depends(get_db)):
    """
    Genera un mensaje de feedback basado en el resultado específico de una partida (id_resultado_juego).
    """

    resultado = db.query(ResultadoJuego).filter(
        ResultadoJuego.id_resultado_juego == id_resultado_juego
    ).first()

    if not resultado:
        raise HTTPException(status_code=404, detail="No se encontró el resultado del juego.")

    correctas = resultado.correctas or 0
    incorrectas = resultado.incorrectas or 0
    total = correctas + incorrectas

    if total == 0:
        return {"mensaje": "No hay respuestas registradas en este resultado."}

    # Calcular el porcentaje de aciertos
    porcentaje = (correctas / total) * 100

    # Generar mensaje de feedback según desempeño
    if porcentaje == 100:
        mensaje = "¡Excelente trabajo! Has respondido todo correctamente 💪"
    elif porcentaje >= 75:
        mensaje = "Muy buen desempeño, sigue así 💪"
    elif porcentaje >= 50:
        mensaje = "Buen intento, puedes mejorar. Repasa los temas donde fallaste 💪"
    else:
        mensaje = "Sería bueno que repases los conceptos básicos antes de volver a intentarlo 💪"


    return {
        "id_resultado_juego": id_resultado_juego,
        "correctas": correctas,
        "incorrectas": incorrectas,
        "porcentaje": porcentaje,
        "mensaje": mensaje
    }