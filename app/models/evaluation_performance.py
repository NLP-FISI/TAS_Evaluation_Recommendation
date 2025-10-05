# app/models/evaluation.py
from pydantic import BaseModel

class RegistroEvaluacionDB(BaseModel):
    """
    Representación de un registro tal como lo solicitaste (campos en español).
    Esto no crea tablas; es un modelo para mapear filas de la BD.
    """
    id_resultado_juego: str
    tiempo_texto_seg: float
    tiempo_pregunta_seg: float
    correctas: int
    incorrectas: int

