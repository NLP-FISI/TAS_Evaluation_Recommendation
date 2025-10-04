from fastapi import APIRouter
from app.services.text_recommendation_service import TextRecommendationService

router = APIRouter(
    prefix="/recommendation-texts",
    tags=["Text Recommendation"]
)

@router.get("/{id_usuario}")
async def get_recommended_texts(id_usuario: int):
    """
    Devuelve los textos recomendados según el grado del usuario.
    """
    return await TextRecommendationService.get_recommended_texts(id_usuario)
