# app/api/v1/evaluation_challenges.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.schemas.evaluation_schemas import RetoParaEvaluar, ResultadoEvaluacion, UsuarioData
from app.services.evaluation_challenges_service import EvaluationChallengeService
from app.core.database import get_db

def get_user_from_db(db: Session, user_id: int) -> UsuarioData:
    # Marcador de posición - Reemplazar con lógica real de SQLAlchemy
    mock_db = {
        101: {"id": 101, "nombre": "Ana", "puntaje_elo": 1600},
        102: {"id": 102, "nombre": "Bruno", "puntaje_elo": 1500}
    }
    user_data = mock_db.get(user_id)
    if not user_data:
        raise HTTPException(status_code=404, detail=f"Usuario con ID {user_id} no encontrado.")
    return UsuarioData(**user_data)

def update_user_elo_in_db(db: Session, user_id: int, new_elo: int):
    # Logica para reemplazar con la actualización real en la base de datos
    # Ejemplo de impresión para simular la actualización
    print(f"ACTUALIZANDO BD: Usuario {user_id} -> Nuevo ELO {new_elo}")
    pass
# ------------------------------------

router = APIRouter(
    prefix="/evaluation-challenges",
    tags=["Evaluation Challenges"]
)

@router.post("/", response_model=ResultadoEvaluacion)
def evaluate_challenge_result(
    data: RetoParaEvaluar, 
    db: Session = Depends(get_db)
):
    """
    Endpoint para realizar la evaluación de un reto competitivo finalizado.
    """
    # 1. Obtener datos de la BD
    retador_data = get_user_from_db(db, data.retador.id_usuario)
    contrincante_data = get_user_from_db(db, data.contrincante.id_usuario)

    # 2. Llamar al método de servicio (siguiendo el patrón de tu compañero)
    resultado_evaluacion = EvaluationChallengeService.procesar_evaluacion_reto(
        data, retador_data, contrincante_data
    )

    # 3. Persistir los cambios en la BD
    update_user_elo_in_db(
        db, 
        resultado_evaluacion.id_retador, 
        resultado_evaluacion.rating_nuevo_retador
    )
    update_user_elo_in_db(
        db, 
        resultado_evaluacion.id_contrincante, 
        resultado_evaluacion.rating_nuevo_contrincante
    )
    
    return resultado_evaluacion