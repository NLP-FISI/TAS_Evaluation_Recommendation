# app/api/v1/recommendation_users.py
from fastapi import APIRouter, Query
from app.services.recommendation_users_service import recomendar_oponentes

router = APIRouter(prefix="/recommendation/users",
                   tags=["Recommendation Users"])


@router.get("/{user_id}", operation_id="get_recommendation_users")
def get_recommendation_users_endpoint(
    user_id: int,
    difficulty: str = Query("equilibrado", enum=[
                            "fácil", "equilibrado", "desafiante"])
):
    """
    Retorna una lista de usuarios recomendados según el nivel de dificultad.
    """
    return recomendar_oponentes(user_id, dificultad=difficulty)
