from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.recommendation_tiers_service import clasificar_jugador
from app.core.database import get_db
from app.models.usuario import Usuario
from app.models.desempenio import Desempenio

router = APIRouter(prefix="/tiers", tags=["Clasificación de Tiers"])


@router.get("/{user_id}")
def obtener_tier(user_id: int, db: Session = Depends(get_db)):
    """
    Endpoint que devuelve el Tier del jugador según sus métricas reales
    almacenadas en la base de datos.
    """

    # Buscar usuario
    usuario = db.query(Usuario).filter(Usuario.id_usuario == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    # Buscar datos de desempeño
    desempenio = db.query(Desempenio).filter(
        Desempenio.id_usuario == user_id).first()
    if not desempenio:
        raise HTTPException(
            status_code=404, detail="No hay datos de desempeño para este usuario.")

    # Preparar datos reales según tu modelo Desempenio
    user_data = {
        "user_id": usuario.id_usuario,
        "nombre": f"{usuario.nombre_usuario} {usuario.apellido_usuario}",
        "nivel_experiencia": float(desempenio.puntaje or 0),
        "consistencia": float(desempenio.exactitud or 0),
        "tiempo_promedio": float(desempenio.promedio_tiempo_por_pregunta or 0),
        "diversificacion": float(desempenio.textos_considerados or 0),
    }

    # Clasificar jugador según el modelo entrenado
    resultado = clasificar_jugador(user_data)

    return {"usuario": resultado}
