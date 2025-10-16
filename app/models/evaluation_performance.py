from pydantic import BaseModel

class RegistroEvaluacionDB(BaseModel):
    """
    Modelo para mapear filas de la BD
    """
    id_resultado_juego: str
    tiempo_texto_seg: float
    tiempo_pregunta_seg: float
    correctas: int
    incorrectas: int

