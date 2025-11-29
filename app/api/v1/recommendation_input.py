from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.recommendation_input_service import RecommendationInputService

router = APIRouter(
    prefix="/api/v1/recommendation-input",
    tags=["Recommendation Input"]
)


@router.get("/{id_usuario}")
async def get_input_recommendations(id_usuario: int, db: Session = Depends(get_db)):
    """
    Devuelve los textos de la prueba de entrada (Fase 1 y Fase 2)
    junto con los datos del usuario.
    """
    data = RecommendationInputService.get_input_texts(id_usuario, db)
    return data
