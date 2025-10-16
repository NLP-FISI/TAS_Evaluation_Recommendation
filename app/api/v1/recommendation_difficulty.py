from fastapi import APIRouter, HTTPException
from app.schemas.recommendation_schemas import TextComplexityRequest, TextComplexityResponse
from app.services.recommendation_difficulty_service import TextComplexityEvaluator

router = APIRouter(prefix="/recommendation/difficulty",
                   tags=["Recommendation - Difficulty"])


@router.post("/evaluate", response_model=TextComplexityResponse)
async def evaluate_content_complexity(request: TextComplexityRequest):
    """
    RF4 - Validación Externa de la Complejidad del Contenido.
    Analiza un texto y devuelve su nivel de complejidad y puntuación cuantitativa.
    """
    try:
        evaluator = TextComplexityEvaluator()
        result = evaluator.evaluate_text(request.content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
