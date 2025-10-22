from fastapi import APIRouter, HTTPException
from app.schemas.recommendation_schemas import RecommendationDifficultyRequest
from app.services.recommendation_difficulty_service import actualizar_dificultad
from app.schemas.recommendation_schemas import TextComplexityRequest, TextComplexityResponse
from app.services.recommendation_difficulty_service import TextComplexityEvaluator


router = APIRouter(prefix="/recommendation/difficulty",
                   tags=["Recommendation - Difficulty"])

#get principal para obtener dificultad_acumulada
@router.get("/difi/{id_user}")
def read_difficulty(id_user: str):
    return {f"dificultad obtenida de {id_user}"}

#get para actualizar dificultad_acumulada

@router.post("/update")
def update_difficulty(request: RecommendationDifficultyRequest, resultado: int):
    theta, racha, beta_next, p = actualizar_dificultad(
        theta=request.accumulated_difficulty,
        racha=request.streak,
        beta=request.challenge_difficulty,
        resultado=resultado
    )

    return {
        "id_user": request.id_user,
        "dificultad_acumulada": round(theta, 3),
        "racha": racha,
        "recomendacion de dificultad": beta_next,
    }

#get para obtener dicicultad_acumulada anterior

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
