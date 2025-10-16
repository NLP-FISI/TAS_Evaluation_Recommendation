# app/api/v1/recommendation_tiers.py
from fastapi import APIRouter
from app.services.recommendation_tiers_service import clasificar_jugador
from faker import Faker
import numpy as np

router = APIRouter(prefix="/tiers", tags=["Clasificación de Tiers"])

fake = Faker()


@router.get("/{user_id}")
def obtener_tier(user_id: int):
    """
    Endpoint que devuelve el Tier del jugador según su nivel de experiencia.
    Datos simulados.
    """
    # Generamos un usuario fake para demostración
    user_data = {
        "user_id": user_id,
        "nombre": fake.first_name(),
        "nivel_experiencia": float(np.clip(np.random.normal(60, 25), 0, 100)),
        "consistencia": float(np.clip(np.random.normal(70, 15), 0, 100)),
        "tiempo_promedio": float(np.clip(np.random.normal(120, 30), 30, 240)),
        "diversificacion": float(np.clip(np.random.normal(65, 25), 0, 100))
    }

    resultado = clasificar_jugador(user_data)
    return {"usuario": resultado}
