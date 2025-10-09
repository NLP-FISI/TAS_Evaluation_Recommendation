from fastapi import APIRouter
from app.schemas.recommendation_schemas import RecommendationDifficultyRequest
from app.services.recommendation_difficulty_service import actualizar_dificultad

router = APIRouter(
    prefix="/recommendation_difficulty",
    tags=["dificultad input"]
)


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

#get para obtener racha
