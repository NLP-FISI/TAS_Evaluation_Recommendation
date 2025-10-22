# app/api/v1/text_recommendation.py
from fastapi import APIRouter
from app.services.text_recommendation_service import TextRecommendationService

router = APIRouter(
    prefix="/recommendation-texts",
    tags=["Text Recommendation"]
)


@router.get("/{id_usuario}")
async def recommend_texts(id_usuario: int):
    """
    Obtiene recomendaciones de texto según el nivel y temática del usuario.
    """
    return await TextRecommendationService.get_recommendations(id_usuario)
