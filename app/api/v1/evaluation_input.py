# File: app/api/v1/evaluation_input.py
from fastapi import APIRouter
from app.schemas.evaluation_schemas import EvaluationInputRequest, EvaluationInputResponse
from app.services.evaluation_input_service import EvaluationInputService

router = APIRouter(
    prefix="/evaluation-input",
    tags=["Evaluation Input"]
)


@router.post("/", response_model=EvaluationInputResponse)
async def evaluate_student(data: EvaluationInputRequest):
    """
    Endpoint para realizar la evaluación inicial de un estudiante.
    """
    return EvaluationInputService.evaluate_student(data)
