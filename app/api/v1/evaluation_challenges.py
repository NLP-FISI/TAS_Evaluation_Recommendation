# File: app/api/v1/evaluation_challenges.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

# Importaciones actualizadas y nuevas
from app.schemas.evaluation_challenges import RetoParaEvaluar, ResultadoEvaluacion, UsuarioData
from app.services.evaluation_challenges_service import EvaluationChallengeService
from app.core.database import get_db
from app.models.evaluation_challenges import Usuario 

router = APIRouter(
    prefix="/evaluation-challenges",
    tags=["Evaluation Challenges"]
)

# --- Las funciones MOCK se eliminan y se reemplazan con la lógica del endpoint ---

@router.post("/", response_model=ResultadoEvaluacion)
def evaluate_challenge_result(
    data: RetoParaEvaluar, 
    db: Session = Depends(get_db)
):
    """
    Endpoint para realizar la evaluación de un reto competitivo finalizado.
    Ahora opera directamente contra la base de datos.
    """
    # 1. Obtener datos REALES de la BD
    retador_db = db.query(Usuario).filter(Usuario.id_usuario == data.retador.id_usuario).first()
    contrincante_db = db.query(Usuario).filter(Usuario.id_usuario == data.contrincante.id_usuario).first()

    # Validar que ambos usuarios existen
    if not retador_db:
        raise HTTPException(status_code=404, detail=f"Usuario retador con ID {data.retador.id_usuario} no encontrado.")
    if not contrincante_db:
        raise HTTPException(status_code=404, detail=f"Usuario contrincante con ID {data.contrincante.id_usuario} no encontrado.")

    # Convertir los modelos SQLAlchemy a esquemas Pydantic para el servicio
    retador_data = UsuarioData.from_attributes(retador_db)
    contrincante_data = UsuarioData.from_attributes(contrincante_db)

    # 2. Llamar al método de servicio (esta parte no cambia)
    resultado_evaluacion = EvaluationChallengeService.procesar_evaluacion_reto(
        data, retador_data, contrincante_data
    )

    # 3. Persistir los cambios en la BD
    retador_db.puntos = resultado_evaluacion.rating_nuevo_retador
    contrincante_db.puntos = resultado_evaluacion.rating_nuevo_contrincante
    
    # Confirmar la transacción para guardar los cambios
    db.commit()
    
    # Opcional: Refrescar los objetos para que reflejen los datos guardados
    db.refresh(retador_db)
    db.refresh(contrincante_db)
    
    return resultado_evaluacion