# app/api/v1/text_recommendation.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.text_recommendation_service import TextRecommendationService
from app.core.database import get_db

router = APIRouter(
    prefix="/recommendation-texts",
    tags=["Text Recommendation"]
)


@router.get("/{id_usuario}")
async def recommend_texts(id_usuario: int, db: Session = Depends(get_db)):
    """
    Obtiene recomendaciones de texto según el nivel y temática del usuario.
    """
    return await TextRecommendationService.get_recommendations(id_usuario, db)
