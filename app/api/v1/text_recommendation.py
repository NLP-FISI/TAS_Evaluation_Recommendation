# app/api/v1/text_recommendation.py
from fastapi import APIRouter, Depends, HTTPException, status
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
    # El servicio se encarga de la lógica y la propagación de errores
    try:
        recommendations = await TextRecommendationService.get_recommendations(id_usuario, db)
        return recommendations
    except HTTPException as e:
        # Re-lanzar la excepción HTTP para que FastAPI la maneje
        raise e
    except Exception as e:
        # Captura cualquier error no manejado y lo devuelve como 500 explícito con detalles
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno no manejado en la ruta: {str(e)}"
        ) from e
