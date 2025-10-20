from pydantic import BaseModel, Field
from typing import List

# Esquema base: representa los datos almacenados en la BD
class RegistroEvaluacionBase(BaseModel):
    id_usuario: int = Field(..., description="ID del estudiante al que pertenece el resultado")
    tiempo_texto_seg: float = Field(..., description="Tiempo de lectura en segundos")
    tiempo_pregunta_seg: float = Field(..., description="Tiempo total en preguntas (s)")
    correctas: int = Field(..., description="Cantidad de preguntas correctas")
    incorrectas: int = Field(..., description="Cantidad de preguntas incorrectas")

    class Config:
        orm_mode = True  # Permite compatibilidad con SQLAlchemy ORM

# Esquema para salida (cuando devuelves datos desde la BD o API)
class RegistroEvaluacionSalida(RegistroEvaluacionBase):
    id_resultado_juego: int = Field(..., description="ID único del resultado del juego")

# Esquema para solicitud (cuando recibes datos de entrada)
class SolicitudEvaluacion(BaseModel):
    id_usuario: int = Field(..., description="ID del estudiante a evaluar")

# Esquema para resultado final del cálculo de evaluación
class ResultadoEvaluacion(BaseModel):
    id_usuario: int
    puntaje: float = Field(..., description="Puntaje (0-100)")
    nivel: str = Field(..., description="Nivel: básico / intermedio / avanzado")
    exactitud: float = Field(..., description="Porcentaje de respuestas correctas (0..1)")
    promedio_tiempo_por_pregunta: float = Field(..., description="Promedio en segundos por pregunta")
    promedio_tiempo_por_lectura: float = Field(..., description="Promedio en segundos por lectura")
    textos_considerados: int = Field(..., description="Cantidad de textos usados en la evaluación")
