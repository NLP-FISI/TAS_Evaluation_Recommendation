# app/api/v1/analisis_respuestas.py
from fastapi import APIRouter
from app.services.analisis_respuestas_service import analizar_desempenio_usuario

router = APIRouter(prefix="/analisis/respuestas",
                   tags=["Análisis de Desempeño"])


@router.get("/{user_id}")
def get_user_responses_analysis(user_id: int):
    """
    Retorna un análisis del desempeño del usuario en las preguntas respondidas,
    mostrando en qué tipo de preguntas tiene más errores o aciertos.
    """
    return analizar_desempenio_usuario(user_id)
