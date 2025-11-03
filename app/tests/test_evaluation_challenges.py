import pytest
from app.services.evaluation_challenges_service import EvaluationChallengeService
from app.schemas.evaluation_challenges import RetoParaEvaluar, DesempenoJugador, UsuarioData

# --- Datos de prueba simulados ---

@pytest.fixture
def usuario_base_retador() -> UsuarioData:
    """Usuario retador con rating base."""
    return UsuarioData(id_usuario=1, nombre_usuario="Retador", puntos=1500)

@pytest.fixture
def usuario_base_contrincante() -> UsuarioData:
    """Usuario contrincante con rating base."""
    return UsuarioData(id_usuario=2, nombre_usuario="Contrincante", puntos=1500)

# --- Casos de prueba para la nueva lógica ---

def test_victoria_simple_retador(usuario_base_retador, usuario_base_contrincante):
    """Prueba una victoria normal del retador sin rachas."""
    print("\n--- Test: Victoria Simple ---")
    desempeno_retador = DesempenoJugador(id_usuario=1, respuestas_correctas=8, tiempo_total_seg=120)
    desempeno_contrincante = DesempenoJugador(id_usuario=2, respuestas_correctas=6, tiempo_total_seg=130)
    
    reto = RetoParaEvaluar(retador=desempeno_retador, contrincante=desempeno_contrincante)
    
    resultado = EvaluationChallengeService.procesar_evaluacion_reto(reto, usuario_base_retador, usuario_base_contrincante)
    
    assert resultado.id_ganador == 1
    assert resultado.variacion_retador == 16  # K/2 para una victoria esperada
    assert resultado.variacion_contrincante == -16
    assert resultado.mensaje_personalizado == "¡Victoria sólida!"
    print(f"Resultado: Retador gana {resultado.variacion_retador} puntos. Mensaje: '{resultado.mensaje_personalizado}'")

def test_victoria_racha_on_fire(usuario_base_retador, usuario_base_contrincante):
    """Prueba una victoria del retador con una racha de 4 victorias."""
    print("\n--- Test: Racha 'On Fire' 🔥 ---")
    desempeno_retador = DesempenoJugador(id_usuario=1, respuestas_correctas=9, tiempo_total_seg=100, racha_victorias=4)
    desempeno_contrincante = DesempenoJugador(id_usuario=2, respuestas_correctas=5, tiempo_total_seg=150)
    
    reto = RetoParaEvaluar(retador=desempeno_retador, contrincante=desempeno_contrincante)
    
    resultado = EvaluationChallengeService.procesar_evaluacion_reto(reto, usuario_base_retador, usuario_base_contrincante)
    
    bonus_esperado = 4  # Bonus por racha de 4
    assert resultado.id_ganador == 1
    assert resultado.variacion_retador == 16 + bonus_esperado
    assert resultado.variacion_contrincante == -16 # El perdedor no tiene bonus
    assert resultado.mensaje_personalizado == "¡Dominante!"
    print(f"Resultado: Retador gana {resultado.variacion_retador} puntos (16 base + {bonus_esperado} bonus). Mensaje: '{resultado.mensaje_personalizado}'")

def test_victoria_remontada(usuario_base_retador, usuario_base_contrincante):
    """Prueba una victoria del retador que rompe una racha de 5 derrotas."""
    print("\n--- Test: Remontada 🚀 ---")
    desempeno_retador = DesempenoJugador(id_usuario=1, respuestas_correctas=7, tiempo_total_seg=110, racha_derrotas=5)
    desempeno_contrincante = DesempenoJugador(id_usuario=2, respuestas_correctas=6, tiempo_total_seg=115)
    
    reto = RetoParaEvaluar(retador=desempeno_retador, contrincante=desempeno_contrincante)
    
    resultado = EvaluationChallengeService.procesar_evaluacion_reto(reto, usuario_base_retador, usuario_base_contrincante)
    
    bonus_esperado = 5 + 5  # 5 base + 5 por racha de derrotas
    assert resultado.id_ganador == 1
    assert resultado.variacion_retador == 16 + bonus_esperado
    assert resultado.variacion_contrincante == -16
    assert resultado.mensaje_personalizado == "¡Buen trabajo!"
    print(f"Resultado: Retador gana {resultado.variacion_retador} puntos (16 base + {bonus_esperado} bonus). Mensaje: '{resultado.mensaje_personalizado}'")

def test_empate(usuario_base_retador, usuario_base_contrincante):
    """Prueba un escenario de empate."""
    print("\n--- Test: Empate ---")
    desempeno_retador = DesempenoJugador(id_usuario=1, respuestas_correctas=8, tiempo_total_seg=120)
    desempeno_contrincante = DesempenoJugador(id_usuario=2, respuestas_correctas=8, tiempo_total_seg=120)
    
    reto = RetoParaEvaluar(retador=desempeno_retador, contrincante=desempeno_contrincante)
    
    resultado = EvaluationChallengeService.procesar_evaluacion_reto(reto, usuario_base_retador, usuario_base_contrincante)
    
    assert resultado.id_ganador is None
    assert resultado.variacion_retador == 0
    assert resultado.variacion_contrincante == 0
    assert resultado.mensaje_personalizado == "¡Empate reñido!"
    print(f"Resultado: Empate. Sin cambios de puntos. Mensaje: '{resultado.mensaje_personalizado}'")
