# app/services/recommendation_users_service.py
from datetime import datetime
from app.models.recommendation import ExperienceLevel
from app.core.database import SessionLocal

def calculate_experience_level(user_id: int, performance: float, consistency: float, diversification: float) -> int:
    """
    Calcula el nivel de experiencia normalizado entre 1 y 100.
    Fórmula ponderada:
    - 50% desempeño
    - 30% consistencia
    - 20% diversificación
    """

    # Normalización (se asume que los inputs están entre 0 y 100)
    weighted_score = (0.5 * performance) + (0.3 * consistency) + (0.2 * diversification)
    level = max(1, min(100, round(weighted_score)))  # Forzamos rango [1, 100]

    # Guardar histórico
    db = SessionLocal()
    experience_record = ExperienceLevel(
        user_id=user_id,
        score=level,
        performance=performance,
        consistency=consistency,
        diversification=diversification,
        created_at=datetime.utcnow()
    )
    db.add(experience_record)
    db.commit()
    db.refresh(experience_record)

    return level
