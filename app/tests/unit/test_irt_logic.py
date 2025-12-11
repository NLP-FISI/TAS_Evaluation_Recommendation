import pytest
import math
from app.services.recommendation_difficulty_service import actualizar_dificultad

# Constantes del algoritmo (eta = 0.6 por defecto)

def test_irt_incremento_estandar_acierto():
    """
    CU01: Verificar que la dificultad (theta) AUMENTE tras un acierto,
    especialmente cuando theta es igual a beta (50% de probabilidad de acierto).
    """
    theta_actual = 3.0   # Habilidad del usuario
    beta_juego = 3.0     # Dificultad del reto
    racha_actual = 0
    resultado = 1        # Acierto
    
    # E(p) = 1 / (1 + exp(-(3.0 - 3.0))) = 0.5. Como acertó (1.0 > 0.5), debe subir.

    nuevo_theta, nueva_racha, beta_siguiente, prob = actualizar_dificultad(
        theta=theta_actual, 
        racha=racha_actual, 
        beta=beta_juego, 
        resultado=resultado
    )
    
    # Validación (Asserts)
    assert nuevo_theta > theta_actual, "Error: La habilidad no aumentó tras el acierto esperado."
    assert nueva_racha == 1, "Error: La racha no se incrementó."
    assert beta_siguiente == 3 or beta_siguiente == 4, "Error: La recomendación siguiente debe ser 3 o 4."


def test_irt_decremento_estandar_error():
    """
    CU02: Verificar que la dificultad (theta) DISMINUYA tras un error,
    especialmente cuando theta es igual a beta.
    """
    theta_actual = 3.0
    beta_juego = 3.0
    racha_actual = 0
    resultado = 0        # Error
    
    # E(p) = 0.5. Como falló (0.0 < 0.5), debe bajar.

    nuevo_theta, nueva_racha, beta_siguiente, prob = actualizar_dificultad(
        theta=theta_actual, 
        racha=racha_actual, 
        beta=beta_juego, 
        resultado=resultado
    )
    
    # Validación (Asserts)
    assert nuevo_theta < theta_actual, "Error: La habilidad no disminuyó tras el error."
    assert nueva_racha == -1, "Error: La racha no se decrementó."
    assert beta_siguiente == 2, "Error: La recomendación siguiente debe ser 2."


def test_irt_limite_superior_5():
    """
    Prueba de Frontera: Asegurar que theta nunca supere 5.0, incluso con racha positiva.
    """
    theta_actual = 4.9 # Valor muy alto, cercano al límite
    beta_juego = 3.0   # Juego fácil, por lo que el impacto del acierto es MÁXIMO
    racha_actual = 3   # Racha máxima (factor * 1.3)
    resultado = 1      # Acierto

    nuevo_theta, _, _, _ = actualizar_dificultad(
        theta=theta_actual, 
        racha=racha_actual, 
        beta=beta_juego, 
        resultado=resultado
    )
    
    # Se espera que el valor sea *forzado* a 5.0 por la función
    assert nuevo_theta <= 5.0, f"Error: Theta excedió el límite de 5.0. Obtenido {nuevo_theta}"
    assert math.isclose(nuevo_theta, 5.0, abs_tol=0.01), "Error: Theta no se limitó correctamente a 5.0."


def test_irt_limite_inferior_1():
    """
    Prueba de Frontera: Asegurar que theta nunca baje de 1.0, incluso con racha negativa.
    """
    theta_actual = 1.1 # Valor muy bajo, cercano al piso
    beta_juego = 5.0   # Juego muy difícil, por lo que el impacto del error es MÁXIMO
    racha_actual = -3  # Racha negativa máxima (factor * 1.3)
    resultado = 0      # Error

    nuevo_theta, _, _, _ = actualizar_dificultad(
        theta=theta_actual, 
        racha=racha_actual, 
        beta=beta_juego, 
        resultado=resultado
    )
    
    # Se espera que el valor sea *forzado* a 1.0 por la función
    assert nuevo_theta >= 1.0, f"Error: Theta cayó por debajo del límite de 1.0. Obtenido {nuevo_theta}"
    assert math.isclose(nuevo_theta, 1.0, abs_tol=0.01), "Error: Theta no se limitó correctamente a 1.0."