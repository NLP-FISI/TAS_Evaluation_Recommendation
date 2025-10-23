# File: app/tests/test_integration_challenges.py
import pytest
from sqlalchemy.orm import Session

from app.services.evaluation_challenges_service import EvaluationChallengeService
from app.schemas.evaluation_challenges import RetoParaEvaluar, DesempenoJugador, UsuarioData
from app.models.evaluation_challenges import Usuario

def test_integracion_victoria_por_aciertos(db_session: Session):
    """
    Prueba el flujo completo con la sintaxis moderna de SQLAlchemy y Pydantic.
    """
    # ARRANGE: Preparar el escenario
    ID_RETADOR = 1
    ID_CONTRINCANTE = 2

    # 1. Obtiene los datos REALES usando el método moderno Session.get()
    #    (Esto corrige la advertencia de SQLAlchemy)
    retador_antes = db_session.get(Usuario, ID_RETADOR)
    contrincante_antes = db_session.get(Usuario, ID_CONTRINCANTE)

    assert retador_antes is not None, f"El usuario con ID {ID_RETADOR} debe existir en la BD de prueba."
    assert contrincante_antes is not None, f"El usuario con ID {ID_CONTRINCANTE} debe existir en la BD de prueba."
    
    elo_inicial_retador = retador_antes.puntos
    elo_inicial_contrincante = contrincante_antes.puntos
    
    # 2. Convierte los modelos SQLAlchemy a Pydantic usando el método moderno model_validate()
    #    (Esto corrige el error AttributeError)
    retador_data = UsuarioData.model_validate(retador_antes)
    contrincante_data = UsuarioData.model_validate(contrincante_antes)

    reto_input = RetoParaEvaluar(
        retador=DesempenoJugador(id_usuario=ID_RETADOR, respuestas_correctas=8, tiempo_total_seg=120.5),
        contrincante=DesempenoJugador(id_usuario=ID_CONTRINCANTE, respuestas_correctas=7, tiempo_total_seg=110.0)
    )

    # ACT: Ejecutar la lógica de negocio
    resultado = EvaluationChallengeService.procesar_evaluacion_reto(reto_input, retador_data, contrincante_data)

    # ASSERT: Verificar el resultado
    assert resultado.id_ganador == ID_RETADOR
    assert resultado.rating_nuevo_retador > elo_inicial_retador
    assert resultado.rating_nuevo_contrincante < elo_inicial_contrincante

    # VERIFICACIÓN EXTRA: Actualizar y comprobar el estado en la sesión
    retador_antes.puntos = resultado.rating_nuevo_retador
    contrincante_antes.puntos = resultado.rating_nuevo_contrincante
    
    db_session.commit()

    retador_actualizado = db_session.get(Usuario, ID_RETADOR)
    assert retador_actualizado.puntos == resultado.rating_nuevo_retador
    
    print(f"\nVictoria por aciertos (Integración): Retador {elo_inicial_retador} -> {retador_actualizado.puntos}")