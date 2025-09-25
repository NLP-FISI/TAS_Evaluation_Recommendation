# This module defines the Pydantic models for handling evaluation input and output data.
from pydantic import BaseModel
from typing import List, Optional


class EvaluationInputRequest(BaseModel):
    student_id: str
    grade_level: int  # Grado escolar (2 - 6)
    preferences: Optional[List[str]] = []  # Ej: ["animales", "aventuras"]


class EvaluationInputResponse(BaseModel):
    student_id: str
    initial_level: str
    recommended_texts: List[str]
    message: str
