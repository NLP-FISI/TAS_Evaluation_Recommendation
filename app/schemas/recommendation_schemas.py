# This module defines the Pydantic models for handling evaluation input and output data.
from pydantic import BaseModel


class RecommendationDifficultyRequest(BaseModel):
    student_id: str
    grade_level: int
    difficulty_id: int

class RecommendationDifficultyResponse(BaseModel):
    student_id: str
    grade_level: int
    difficulty_id: int