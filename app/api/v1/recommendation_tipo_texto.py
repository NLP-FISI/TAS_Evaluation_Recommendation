from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.usuario import Usuario
from app.services.recommendation_tipo_texto_service import recomendar_tipo_texto, entrenar_modelo_tipo_texto

router = APIRouter(prefix="/recommendation-text-type",
                   tags=["Recomendación Tipo de Texto"])

# Entrenamos o cargamos el modelo al inicio
entrenar_modelo_tipo_texto()


@router.get("/{user_id}")
def obtener_tipo_texto_recomendado(user_id: int, db: Session = Depends(get_db)):
    """
    Retorna el tipo de texto recomendado (id y nombre) para el usuario.
    """

    usuario = db.query(Usuario).filter(Usuario.id_usuario == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    resultado = recomendar_tipo_texto(usuario, db)
    return {"tipo_texto_recomendado": resultado}
