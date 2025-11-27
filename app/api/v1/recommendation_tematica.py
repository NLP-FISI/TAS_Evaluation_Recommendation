# app/api/v1/recommendation_tematica.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.recommendation_tematica_service import recomendar_tematica

router = APIRouter(prefix="/tematica", tags=["Recomendación de Temática"])


@router.get("/recomendar/{user_id}")
def obtener_tematica_recomendada(user_id: int, db: Session = Depends(get_db)):
    """
    Devuelve la temática más recomendada para el usuario
    basándose en su perfil y similitud con otros usuarios.
    """
    tematica = recomendar_tematica(user_id, db)
    if not tematica:
        raise HTTPException(
            status_code=404, detail="No se pudo recomendar una temática para este usuario.")

    return {
        "id_tematica": tematica.id_tematica,
        "nombre_tematica": tematica.nombre_tematica
    }
