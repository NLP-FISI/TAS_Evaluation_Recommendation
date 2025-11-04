# File: app/api/v1/evaluation_challenges.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

# Importaciones actualizadas y nuevas
from app.schemas.evaluation_challenges import RetoParaEvaluar, ResultadoEvaluacion, UsuarioData
from app.services.evaluation_challenges_service import EvaluationChallengeService
from app.core.database import get_db
from app.models.usuario import Usuario 
from app.models.juego import Juego
from app.models.reto import Reto
import datetime

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
    # En Pydantic v2 la forma correcta de validar objetos con atributos es
    # usar `model_validate(..., from_attributes=True)` o configurar
    # `model_config = ConfigDict(from_attributes=True)` en el modelo.
    # Evitamos usar el inexistente método `from_attributes`.
    retador_data = UsuarioData.model_validate(retador_db, from_attributes=True)
    contrincante_data = UsuarioData.model_validate(contrincante_db, from_attributes=True)

    # 1. Calcular las rachas desde la BD
    racha_v_retador, racha_d_retador = EvaluationChallengeService._get_user_streak(data.retador.id_usuario, db)
    racha_v_contrincante, racha_d_contrincante = EvaluationChallengeService._get_user_streak(data.contrincante.id_usuario, db)

    # 2. Llamar al servicio de evaluación pasando las rachas
    resultado_evaluacion = EvaluationChallengeService.procesar_evaluacion_reto(
        reto_input=data, 
        retador_data=retador_data, 
        contrincante_data=contrincante_data,
        racha_victorias_retador=racha_v_retador,
        racha_derrotas_retador=racha_d_retador,
        racha_victorias_contrincante=racha_v_contrincante,
        racha_derrotas_contrincante=racha_d_contrincante
    )

    # 3. Persistir los cambios de puntos en la BD
    retador_db.puntos = resultado_evaluacion.rating_nuevo_retador
    contrincante_db.puntos = resultado_evaluacion.rating_nuevo_contrincante
    
    # 4. Crear un nuevo registro del juego y del reto finalizado
    nuevo_juego = Juego(
        id_tipo_juego=2, # Asumimos que 2 es 'Reto'
        fecha_creacion=datetime.datetime.utcnow(),
        activo=False,
        # --- VALOR CORREGIDO ---
        nombre_juego=["Reto Competitivo"] # Se pasa como una lista
    )
    db.add(nuevo_juego)
    db.flush() # Para obtener el id_juego generado

    nuevo_reto = Reto(
        id_juego=nuevo_juego.id_juego,
        id_usuario_retador=data.retador.id_usuario,
        id_usuario_contrincante=data.contrincante.id_usuario,
        estado='finalizado',
        ganador=resultado_evaluacion.id_ganador
    )
    db.add(nuevo_reto)
    
    db.commit()
    
    return resultado_evaluacion