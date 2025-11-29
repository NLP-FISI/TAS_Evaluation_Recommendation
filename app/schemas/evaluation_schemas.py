# This module defines the Pydantic models for handling evaluation input and output data.
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from enum import Enum


class EvaluationInputRequest(BaseModel):
    student_id: str
    grade_level: int  # Grado escolar (2 - 6)
    preferences: Optional[List[str]] = []  # Ej: ["animales", "aventuras"]


class AlternativeInfo(BaseModel):
    """Información de una alternativa."""
    alternative_id: int
    text: str


class QuestionInfo(BaseModel):
    """Información de una pregunta con sus alternativas."""
    question_id: int
    question_text: str
    alternatives: List[AlternativeInfo]


class TextWithQuestions(BaseModel):
    """Texto con sus preguntas y alternativas."""
    text_id: int
    title: str
    content: str
    format: str = "plain"  # "plain" o "html"
    questions: List[QuestionInfo]


class EvaluationInputResponse(BaseModel):
    student_id: str
    initial_level: str
    texts: List[TextWithQuestions]  # Textos con preguntas
    message: str

# =====================================================================================
# == ESQUEMAS PARA LA EVALUACIÓN DE RETOS COMPETITIVOS ==
# =====================================================================================

class RetoResultadoEnum(str, Enum):
    victoria_retador = "victoria_retador"
    victoria_contrincante = "victoria_contrincante"
    empate = "empate"

class DesempenoJugador(BaseModel):
    id_usuario: int = Field(..., description="ID único del jugador.")
    respuestas_correctas: int = Field(..., ge=0, description="Número de respuestas correctas.")
    tiempo_total_seg: float = Field(..., ge=0, description="Tiempo total en segundos que tardó en responder.")

class RetoParaEvaluar(BaseModel):
    retador: DesempenoJugador
    contrincante: DesempenoJugador
    
class ResultadoEvaluacion(BaseModel):
    id_ganador: int | None = Field(description="ID del jugador ganador. Nulo si es empate.")
    
    id_retador: int
    rating_anterior_retador: int
    rating_nuevo_retador: int
    variacion_retador: int

    id_contrincante: int
    rating_anterior_contrincante: int
    rating_nuevo_contrincante: int
    variacion_contrincante: int
    
    mensaje: str

class UsuarioData(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre: str
    puntaje_elo: int