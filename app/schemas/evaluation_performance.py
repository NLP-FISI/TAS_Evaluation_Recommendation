# app/schemas/evaluation_schemas.py
from pydantic import BaseModel, Field
from typing import List

class RegistroEvaluacionSalida(BaseModel):
    id_resultado_juego: str = Field(..., description="ID del texto")
    tiempo_texto_seg: float = Field(..., description="Tiempo de lectura en segundos")
    tiempo_pregunta_seg: float = Field(..., description="Tiempo total en preguntas (s)")
    correctas: int = Field(..., description="Cantidad de preguntas correctas")
    incorrectas: int = Field(..., description="Cantidad de preguntas incorrectas")

class SolicitudEvaluacion(BaseModel):
    id_usuario: str = Field(..., description="ID del estudiante a evaluar")

class ResultadoEvaluacion(BaseModel):
    id_usuario: str
    puntaje: float = Field(..., description="Puntaje (0-100)")
    nivel: str = Field(..., description="Nivel: básico / intermedio / avanzado")
    exactitud: float = Field(..., description="Porcentaje de respuestas correctas (0..1)")
    promedio_tiempo_por_pregunta: float = Field(..., description="s")
    promedio_tiempo_por_lectura: float = Field(..., description="s")
    textos_considerados: int = Field(..., description="Cantidad de textos usados")
