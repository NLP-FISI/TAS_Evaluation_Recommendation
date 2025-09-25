# This module defines the Pydantic models for handling diagnostic test data.
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class DifficultLevel(str, Enum):
    BASIC = "básico"
    INTERMEDIATE = "intermedio"
    ADVANCED = "avanzado"


class QuestionType(str, Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    TEXT_COMPREHENSION = "text_comprehension"


class DiagnosticQuestion(BaseModel):
    question_id: str
    question_text: str
    question_type: QuestionType
    options: Optional[List[str]] = None  # For multiple choice questions
    correct_answer: str
    skill_area: str  # e.g., "comprensión_lectora", "vocabulario", "gramática"
    difficulty_level: DifficultLevel


class DiagnosticTestRequest(BaseModel):
    student_id: str
    grade_level: int  # Grado escolar (2 - 6)
    test_level: DifficultLevel = DifficultLevel.BASIC  # Default to basic for Stage 1
    preferences: Optional[List[str]] = []  # Student preferences for content themes


class StudentAnswer(BaseModel):
    question_id: str
    answer: str
    time_spent: Optional[int] = None  # Time spent in seconds


class DiagnosticTestSubmission(BaseModel):
    student_id: str
    test_id: str
    answers: List[StudentAnswer]


class SkillAssessment(BaseModel):
    skill_area: str
    score: float  # 0.0 to 1.0
    level: DifficultLevel
    strengths: List[str]
    weaknesses: List[str]


class DiagnosticTestResponse(BaseModel):
    student_id: str
    test_id: str
    questions: List[DiagnosticQuestion]
    instructions: str
    time_limit: int  # Time limit in minutes


class DiagnosticResultsResponse(BaseModel):
    student_id: str
    test_id: str
    overall_score: float  # 0.0 to 1.0
    overall_level: DifficultLevel
    skill_assessments: List[SkillAssessment]
    recommendations: List[str]
    next_steps: List[str]
    message: str