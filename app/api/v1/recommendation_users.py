from fastapi import APIRouter, Query
from app.services.recommendation_users_service import recomendar_oponentes

router = APIRouter(prefix="/recommendation/users",
                   tags=["Recommendation Users"])


@router.get("/{user_id}")
def get_recommended_users(
    user_id: int,
    difficulty: str = Query("equilibrado", enum=[
                            "fácil", "equilibrado", "desafiante"])
):
    """
    Retorna una lista de usuarios recomendados según el nivel de dificultad.
    """
    return recomendar_oponentes(user_id, dificultad=difficulty)
