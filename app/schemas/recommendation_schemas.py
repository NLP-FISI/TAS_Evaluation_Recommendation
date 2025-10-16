# app/schemas/recommendation_schemas.py
from pydantic import BaseModel
from datetime import datetime


class ExperienceLevelResponse(BaseModel):
    user_id: int
    score: int
    performance: float
    consistency: float
    diversification: float
    created_at: datetime

    class Config:
        orm_mode = True
