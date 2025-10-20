# app/schemas/evaluation_analytics_schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class AnswerItem(BaseModel):
    question_id: int
    type: str  # 'literal' | 'inferencial' | 'critico' (otras variantes serán normalizadas)
    is_correct: bool


class EvaluationAnalyticsRequest(BaseModel):
    """
    request puede contener:
      - answers: lista detallada (recomendada)
      - counts: conteos agregados por tipo (alternativa)
    """
    student_id: str
    answers: Optional[List[AnswerItem]] = None
    counts: Optional[Dict[str, Dict[str, int]]] = None  # formato: {"literal": {"correct":3,"total":5}, ...}


class EvaluationAnalyticsResponse(BaseModel):
    student_id: str
    performance: Dict[str, float] = Field(..., description="porcentajes por tipo: literal/inferencial/critico")
    overall_level: str = Field(..., description="Nivel global: Alto/Medio/Bajo")
    recommendations: List[str] = Field(..., description="Lista de recomendaciones detalladas")
    message: Optional[str] = Field("Análisis completado.")
