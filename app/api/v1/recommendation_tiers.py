# app/api/v1/recommendation_tiers.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.recommendation_tiers_service import entrenar_y_clasificar
from app.core.database import get_db
from app.models.usuario import Usuario
from app.models.desempenio import Desempenio
import pandas as pd

router = APIRouter(prefix="/tiers", tags=["Clasificación de Tiers"])


@router.get("/{user_id}")
def obtener_tier(user_id: int, db: Session = Depends(get_db)):
    """
    Endpoint que devuelve el Tier del jugador según sus métricas reales
    almacenadas en la base de datos.
    Entrena el modelo temporalmente con los datos de la tabla Desempenio.
    """

    # --- Buscar usuario ---
    usuario = db.query(Usuario).filter(Usuario.id_usuario == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    # --- Obtener todos los desempeños para entrenar el modelo ---
    desempenios = db.query(Desempenio).all()
    if not desempenios:
        raise HTTPException(
            status_code=404, detail="No hay registros de desempeño en la base de datos.")

    # --- Convertir los registros a un DataFrame ---
    df = pd.DataFrame([
        {
            "nivel_experiencia": d.puntaje or 0,
            "consistencia": d.exactitud or 0,
            "tiempo_promedio": d.promedio_tiempo_por_pregunta or 0,
            "diversificacion": d.textos_considerados or 0,
        }
        for d in desempenios
    ])

    # --- Crear etiquetas (tiers) para entrenamiento ---
    def etiquetar_tier(puntaje):
        if puntaje <= 30:
            return "Principiante"
        elif puntaje <= 60:
            return "Intermedio"
        elif puntaje <= 85:
            return "Avanzado"
        else:
            return "Experto"

    df["tier"] = df["nivel_experiencia"].apply(etiquetar_tier)

    # --- Buscar el desempeño del usuario actual ---
    desempenio_usuario = next(
        (d for d in desempenios if d.id_usuario == user_id), None)
    if not desempenio_usuario:
        raise HTTPException(
            status_code=404, detail="No hay datos de desempeño para este usuario.")

    # --- Datos del usuario a clasificar ---
    user_data = {
        "user_id": usuario.id_usuario,
        "nombre": f"{usuario.nombre_usuario} {usuario.apellido_usuario}",
        "nivel_experiencia": float(desempenio_usuario.puntaje or 0),
        "consistencia": float(desempenio_usuario.exactitud or 0),
        "tiempo_promedio": float(desempenio_usuario.promedio_tiempo_por_pregunta or 0),
        "diversificacion": float(desempenio_usuario.textos_considerados or 0),
    }

    # --- Clasificar jugador entrenando el modelo en memoria ---
    resultado = entrenar_y_clasificar(df, user_data)

    return {"usuario": resultado}
