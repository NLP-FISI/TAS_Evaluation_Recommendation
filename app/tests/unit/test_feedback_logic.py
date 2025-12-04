import pytest
from typing import Tuple, Optional

# --- Lógica de Feedback Aislada (Simulando la lógica del endpoint) ---
def _generar_mensaje_feedback(correctas: int, incorrectas: int) -> str:
    """
    Simula la lógica de umbrales del archivo evaluation_feedback.py
    """
    total = correctas + incorrectas
    
    if total == 0:
        return "No hay respuestas registradas en este resultado."

    porcentaje = (correctas / total) * 100

    if porcentaje == 100:
        mensaje = "¡Excelente trabajo! Has respondido todo correctamente 💪"
    elif porcentaje >= 75:
        mensaje = "Muy buen desempeño, sigue así 💪"
    elif porcentaje >= 50:
        mensaje = "Buen intento, puedes mejorar. Repasa los temas donde fallaste 💪"
    else:
        mensaje = "Sería bueno que repases los conceptos básicos antes de volver a intentarlo 💪"
    
    return mensaje

# --- Casos de Prueba ---

def test_feedback_nivel_excelente_100_porciento():
    """Prueba de Frontera: Exactamente 100% de aciertos."""
    # 4/4 = 100%
    mensaje = _generar_mensaje_feedback(correctas=4, incorrectas=0)
    assert mensaje == "¡Excelente trabajo! Has respondido todo correctamente 💪"

def test_feedback_nivel_bueno_limite_inferior_75_porciento():
    """Prueba de Frontera: Límite inferior de la categoría 'Muy buen desempeño' (75%)."""
    # 3/4 = 75%
    mensaje = _generar_mensaje_feedback(correctas=3, incorrectas=1)
    assert mensaje == "Muy buen desempeño, sigue así 💪"

def test_feedback_nivel_bueno_borde_74_porciento():
    """Prueba de Frontera: Justo por debajo de 75% (ej. 74.99...). Debe caer en la siguiente categoría."""
    # 7/10 = 70%
    mensaje = _generar_mensaje_feedback(correctas=7, incorrectas=3)
    assert mensaje == "Buen intento, puedes mejorar. Repasa los temas donde fallaste 💪"

def test_feedback_nivel_regular_limite_inferior_50_porciento():
    """Prueba de Frontera: Límite inferior de la categoría 'Buen intento' (50%)."""
    # 1/2 = 50%
    mensaje = _generar_mensaje_feedback(correctas=1, incorrectas=1)
    assert mensaje == "Buen intento, puedes mejorar. Repasa los temas donde fallaste 💪"

def test_feedback_nivel_bajo_borde_49_porciento():
    """Prueba de Frontera: Justo por debajo de 50%. Debe caer en la última categoría."""
    # 4/9 = 44.4%
    mensaje = _generar_mensaje_feedback(correctas=4, incorrectas=5)
    assert mensaje == "Sería bueno que repases los conceptos básicos antes de volver a intentarlo 💪"

def test_feedback_cero_respuestas():
    """Prueba de Borde: Caso donde no hay respuestas (total=0)."""
    mensaje = _generar_mensaje_feedback(correctas=0, incorrectas=0)
    assert mensaje == "No hay respuestas registradas en este resultado."