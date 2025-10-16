# app/api/v1/evaluation_analytics.py
from fastapi import APIRouter, HTTPException
from app.schemas.evaluation_analytics_schemas import (
    EvaluationAnalyticsRequest,
    EvaluationAnalyticsResponse,
)
from app.services.evaluation_analytics_service import EvaluationAnalyticsService

router = APIRouter(
    prefix="/evaluation-analytics",
    tags=["Evaluation Analytics"]
)


@router.post("/", response_model=EvaluationAnalyticsResponse)
async def analyze_student_performance(data: EvaluationAnalyticsRequest):
    """
    Endpoint NUEVO e independiente para análisis (métricas + recomendaciones).
    No modifica /evaluation-input ni otros endpoints.
    """
    try:
        result = EvaluationAnalyticsService.analyze(data)
        return result
    except Exception as e:
        # Devolver error 400 con mensaje claro
        raise HTTPException(status_code=400, detail=str(e))
