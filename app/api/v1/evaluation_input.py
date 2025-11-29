# File: app/api/v1/evaluation_input.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.evaluation_schemas import EvaluationInputRequest, EvaluationInputResponse
from app.services.evaluation_input_service import EvaluationInputService
from app.core.database import get_db

router = APIRouter(
    prefix="/evaluation-input",
    tags=["Evaluation Input"]
)


@router.post("/", response_model=EvaluationInputResponse)
async def evaluate_student(
    data: EvaluationInputRequest,
    db: Session = Depends(get_db)
):
    """
    Endpoint para realizar la evaluación inicial de un estudiante.
    Devuelve los dos primeros textos de diagnóstico (ID 1 y 2) con sus preguntas y alternativas.
    """
    return EvaluationInputService.evaluate_student(data, db)
