# app/schemas/recommendation_schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Dict


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
