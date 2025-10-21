# This module defines the Pydantic models for handling evaluation input and output data.
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict

class RecommendationDifficultyRequest(BaseModel):
    id_user: int = Field(..., description="Identificador único del usuario")
    streak: int = Field(..., ge=-3, le=3, description="Racha actual (-3 a +3)")
    accumulated_difficulty: float = Field(..., ge=1, le=5, description="Dificultad acumulada (1 a 5)")
    challenge_difficulty: int = Field(..., ge=1, le=5, description="Dificultad del reto anterior (1 a 5)")
      
class RecommendationDifficultyResponse(BaseModel):
    student_id: str
    grade_level: int
    difficulty_id: int
# app/schemas/recommendation_schemas.py


class ExperienceLevelResponse(BaseModel):
    user_id: int
    score: int
    performance: float
    consistency: float
    diversification: float
    created_at: datetime

    class Config:
        orm_mode = True


class TextComplexityRequest(BaseModel):
    content: str


class TextComplexityResponse(BaseModel):
    score: float
    level: str
    metrics: Dict[str, float]
