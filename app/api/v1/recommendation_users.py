# app/api/v1/recommendation_users.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.recommendation_schemas import ExperienceLevelResponse
from app.services.recommendation_users_service import calculate_experience_level

router = APIRouter()

@router.get("/experience-level/{user_id}", response_model=ExperienceLevelResponse)
def get_experience_level(user_id: int, db: Session = Depends(get_db)):
    """
    Calcula y retorna el nivel de experiencia de un usuario.
    (Aquí podrías traer métricas históricas reales desde BD,
    por ahora se usan valores simulados.)
    """
    # 🔹 TODO: Reemplazar con queries reales a métricas
    performance = 75.0
    consistency = 60.0
    diversification = 50.0

    score = calculate_experience_level(user_id, performance, consistency, diversification)

    return {
        "user_id": user_id,
        "score": score,
        "performance": performance,
        "consistency": consistency,
        "diversification": diversification,
        "created_at": None  # será sobreescrito en el servicio
    }
