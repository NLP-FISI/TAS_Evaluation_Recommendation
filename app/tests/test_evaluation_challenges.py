import pytest
from app.services import evaluation_challenges_service as services
from app.schemas.evaluation_schemas import RetoParaEvaluar, DesempenoJugador, UsuarioData

# --- DATOS DE PRUEBA (SIMULACIÓN) ---
# Definimos los datos de los jugadores que usaremos en múltiples pruebas
@pytest.fixture
def ana() -> UsuarioData:
    return UsuarioData(id=101, nombre="Ana", puntaje_elo=1600.0)

@pytest.fixture
def bruno() -> UsuarioData:
    return UsuarioData(id=102, nombre="Bruno", puntaje_elo=1500.0)

# --- CASOS DE PRUEBA ---
def test_evaluacion_victoria_por_aciertos(ana, bruno):
    """Prueba un escenario donde el retador (Ana) gana por más aciertos."""
    reto_input = RetoParaEvaluar(
        retador=DesempenoJugador(id_usuario=ana.id, respuestas_correctas=8, tiempo_total_seg=120.5),
        contrincante=DesempenoJugador(id_usuario=bruno.id, respuestas_correctas=7, tiempo_total_seg=110.0)
    )
    
    resultado = services.EvaluationChallengeService.procesar_evaluacion_reto(reto_input, ana, bruno)
    
    assert resultado.id_ganador == ana.id
    assert resultado.rating_nuevo_retador > ana.puntaje_elo
    assert resultado.rating_nuevo_contrincante < bruno.puntaje_elo
    print(f"\nVictoria por aciertos: Ana {ana.puntaje_elo:.0f} -> {resultado.rating_nuevo_retador:.2f}")

def test_evaluacion_victoria_por_tiempo(ana, bruno):
    """Prueba un empate en aciertos donde el contrincante (Bruno) gana por ser más rápido."""
    reto_input = RetoParaEvaluar(
        retador=DesempenoJugador(id_usuario=ana.id, respuestas_correctas=9, tiempo_total_seg=105.8),
        contrincante=DesempenoJugador(id_usuario=bruno.id, respuestas_correctas=9, tiempo_total_seg=95.2)
    )

    resultado = services.EvaluationChallengeService.procesar_evaluacion_reto(reto_input, ana, bruno)
    
    assert resultado.id_ganador == bruno.id
    assert resultado.rating_nuevo_contrincante > bruno.puntaje_elo
    assert resultado.rating_nuevo_retador < ana.puntaje_elo
    print(f"\nVictoria por tiempo: Bruno {bruno.puntaje_elo:.0f} -> {resultado.rating_nuevo_contrincante:.2f}")

def test_evaluacion_empate_absoluto(ana, bruno):
    """Prueba un empate perfecto entre dos jugadores."""
    reto_input = RetoParaEvaluar(
        retador=DesempenoJugador(id_usuario=ana.id, respuestas_correctas=10, tiempo_total_seg=90.0),
        contrincante=DesempenoJugador(id_usuario=bruno.id, respuestas_correctas=10, tiempo_total_seg=90.0)
    )

    resultado = services.EvaluationChallengeService.procesar_evaluacion_reto(reto_input, ana, bruno)

    assert resultado.id_ganador is None
    # Cuando un jugador de mayor ELO empata, pierde puntos.
    assert resultado.rating_nuevo_retador < ana.puntaje_elo
    assert resultado.rating_nuevo_contrincante > bruno.puntaje_elo
    print(f"\nEmpate: Ana {ana.puntaje_elo:.0f} -> {resultado.rating_nuevo_retador:.2f}, Bruno {bruno.puntaje_elo:.0f} -> {resultado.rating_nuevo_contrincante:.2f}")