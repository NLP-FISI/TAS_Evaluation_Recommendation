import pytest
# Importamos la función de cálculo ELO directamente desde el servicio
from app.services.evaluation_challenges_service import EvaluationChallengeService

# Usamos el K-Factor por defecto del servicio, que es 32

def test_elo_victoria_estandar_mismos_puntos():
    """
    Escenario 1: Ambos jugadores tienen los mismos puntos (1500 vs 1500).
    El Jugador A gana (score_a = 1.0).
    Resultado esperado: El ganador A recibe +16, el perdedor B recibe -16.
    """
    rating_a = 1500
    rating_b = 1500
    score_a = 1.0 # A gana

    new_rating_a, new_rating_b = EvaluationChallengeService._calculate_new_elo_ratings(
        rating_a, rating_b, score_a
    )
    
    # Assert (Validaciones)
    assert new_rating_a == 1516
    assert new_rating_b == 1484

def test_elo_empate_mismos_puntos():
    """
    Escenario 2: Ambos jugadores tienen los mismos puntos y empatan.
    El score esperado para A y B es 0.5.
    Resultado esperado: No hay cambio de puntos (0).
    """
    rating_a = 1500
    rating_b = 1500
    score_a = 0.5 # Empate

    new_rating_a, new_rating_b = EvaluationChallengeService._calculate_new_elo_ratings(
        rating_a, rating_b, score_a
    )
    
    # Assert
    assert new_rating_a == 1500
    assert new_rating_b == 1500


def test_elo_victoria_facil_gran_ganancia():
    """
    Escenario 3: El jugador DEBIL (A=1200) le gana al jugador FUERTE (B=1500).
    La ganancia de puntos para A debe ser MAYOR a 16.
    """
    rating_a = 1200 # Jugador A (Debil)
    rating_b = 1500 # Jugador B (Fuerte)
    score_a = 1.0 # A gana

    new_rating_a, new_rating_b = EvaluationChallengeService._calculate_new_elo_ratings(
        rating_a, rating_b, score_a
    )
    
    # La ganancia es grande (aprox 28 puntos) porque A hizo un "upset"
    assert new_rating_a > 1500, f"Error: La ganancia debería ser mayor a 16. Obtenido {new_rating_a - 1200}"
    assert new_rating_a == 1251

def test_elo_victoria_dificil_poca_ganancia():
    """
    Escenario 4: El jugador FUERTE (A=1500) le gana al jugador DEBIL (B=1200).
    La ganancia de puntos para A debe ser MENOR a 16 (porque era un resultado esperado).
    """
    rating_a = 1500 # Jugador A (Fuerte)
    rating_b = 1200 # Jugador B (Debil)
    score_a = 1.0 # A gana

    new_rating_a, new_rating_b = EvaluationChallengeService._calculate_new_elo_ratings(
        rating_a, rating_b, score_a
    )
    
    # La ganancia es pequeña (aprox 4 puntos)
    assert new_rating_a < 1516, f"Error: La ganancia debería ser menor a 16. Obtenido {new_rating_a - 1500}"
    assert new_rating_a == 1504