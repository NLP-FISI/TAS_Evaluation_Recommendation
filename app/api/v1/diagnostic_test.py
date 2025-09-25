# This module defines API endpoints for diagnostic testing functionality
from fastapi import APIRouter, HTTPException
from app.schemas.diagnostic_schemas import (
    DiagnosticTestRequest, DiagnosticTestResponse, DiagnosticTestSubmission,
    DiagnosticResultsResponse
)
from app.services.diagnostic_test_service import DiagnosticTestService

router = APIRouter(
    prefix="/diagnostic-test",
    tags=["Diagnostic Test"]
)


@router.post("/generate", response_model=DiagnosticTestResponse)
async def generate_diagnostic_test(data: DiagnosticTestRequest):
    """
    Genera una prueba de diagnóstico para un estudiante.
    
    Para la Etapa 1 (Nivel Básico), se genera un test con preguntas fundamentales
    de comprensión lectora, vocabulario y gramática básica.
    """
    try:
        return DiagnosticTestService.generate_diagnostic_test(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando la prueba diagnóstica: {str(e)}")


@router.post("/evaluate", response_model=DiagnosticResultsResponse)
async def evaluate_diagnostic_test(submission: DiagnosticTestSubmission):
    """
    Evalúa las respuestas de un estudiante en la prueba diagnóstica.
    
    Analiza el desempeño en diferentes áreas de habilidades y proporciona:
    - Puntuación general
    - Nivel diagnosticado
    - Evaluación por áreas de habilidades
    - Recomendaciones personalizadas
    - Próximos pasos sugeridos
    """
    try:
        return DiagnosticTestService.evaluate_diagnostic_test(submission)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluando la prueba diagnóstica: {str(e)}")


@router.get("/questions/basic")
async def get_basic_level_questions():
    """
    Endpoint de utilidad para obtener las preguntas de nivel básico.
    Útil para desarrollo y testing.
    """
    try:
        questions = DiagnosticTestService._get_basic_level_questions()
        return {"questions": questions, "total": len(questions)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo preguntas básicas: {str(e)}")