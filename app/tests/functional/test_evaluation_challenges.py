import pytest
from app.services.evaluation_challenges_service import EvaluationChallengeService
from app.schemas.evaluation_challenges import RetoParaEvaluar, DesempenoJugador, UsuarioData
from datetime import datetime
from app.models.usuario import Usuario
from app.models.juego import Juego
from app.models.reto import Reto
from app.models.grado import Grado
from app.models.tipo_texto import TipoTexto
from app.models.tematica import Tematica
from app.models.dificultad import Dificultad
from app.models.escenario import Escenario
from app.models.tipo_juego import TipoJuego
from app.models.nivel import Nivel
from app.models.recompensa import Recompensa
from sqlalchemy import text

# --- Datos de prueba (sin cambios) ---
@pytest.fixture
def usuario_base_retador() -> UsuarioData:
    return UsuarioData(id_usuario=1, nombre_usuario="Retador", puntos=1500)

@pytest.fixture
def usuario_base_contrincante() -> UsuarioData:
    return UsuarioData(id_usuario=2, nombre_usuario="Contrincante", puntos=1500)

# --- Casos de prueba (CORREGIDOS) ---

def test_victoria_simple_retador(db_session, usuario_base_retador, usuario_base_contrincante):
    """Prueba una victoria normal sin rachas."""
    print("\n--- Test: Victoria Simple ---")
    desempeno_retador = DesempenoJugador(id_usuario=1, respuestas_correctas=8, tiempo_total_seg=120)
    desempeno_contrincante = DesempenoJugador(id_usuario=2, respuestas_correctas=6, tiempo_total_seg=130)
    reto = RetoParaEvaluar(retador=desempeno_retador, contrincante=desempeno_contrincante)
    
    # Se pasan las rachas como argumentos
    resultado = EvaluationChallengeService.procesar_evaluacion_reto(
        reto, usuario_base_retador, usuario_base_contrincante,
        racha_victorias_retador=0, racha_derrotas_retador=0,
        racha_victorias_contrincante=0, racha_derrotas_contrincante=0
    )
    
    assert resultado.id_ganador == 1
    assert resultado.variacion_retador == 16
    assert resultado.mensaje_personalizado == "¡Muy bien! 👍"
    print(f"Resultado: Retador gana {resultado.variacion_retador} puntos. Mensaje: '{resultado.mensaje_personalizado}'")

def test_victoria_racha_on_fire(db_session, usuario_base_retador, usuario_base_contrincante):
    """Prueba una victoria con una racha simulada de 4 victorias."""
    print("\n--- Test: Racha 'On Fire' 🔥 ---")
    # Ya no se pasa la racha en DesempenoJugador
    desempeno_retador = DesempenoJugador(id_usuario=1, respuestas_correctas=9, tiempo_total_seg=100)
    desempeno_contrincante = DesempenoJugador(id_usuario=2, respuestas_correctas=5, tiempo_total_seg=150)
    reto = RetoParaEvaluar(retador=desempeno_retador, contrincante=desempeno_contrincante)
    
    # Se simula la racha pasándola como argumento
    resultado = EvaluationChallengeService.procesar_evaluacion_reto(
        reto, usuario_base_retador, usuario_base_contrincante,
        racha_victorias_retador=4, racha_derrotas_retador=0,
        racha_victorias_contrincante=0, racha_derrotas_contrincante=0
    )
    
    bonus_esperado = 4
    assert resultado.id_ganador == 1
    assert resultado.variacion_retador == 16 + bonus_esperado
    assert resultado.mensaje_personalizado == "¡Imparable! 🔥"
    print(f"Resultado: Retador gana {resultado.variacion_retador} puntos (16 base + {bonus_esperado} bonus). Mensaje: '{resultado.mensaje_personalizado}'")

def test_victoria_remontada(db_session, usuario_base_retador, usuario_base_contrincante):
    """Prueba una victoria que rompe una racha de 5 derrotas."""
    print("\n--- Test: Remontada 🚀 ---")
    desempeno_retador = DesempenoJugador(id_usuario=1, respuestas_correctas=7, tiempo_total_seg=110)
    desempeno_contrincante = DesempenoJugador(id_usuario=2, respuestas_correctas=6, tiempo_total_seg=115)
    reto = RetoParaEvaluar(retador=desempeno_retador, contrincante=desempeno_contrincante)
    
    resultado = EvaluationChallengeService.procesar_evaluacion_reto(
        reto, usuario_base_retador, usuario_base_contrincante,
        racha_victorias_retador=0, racha_derrotas_retador=5,
        racha_victorias_contrincante=0, racha_derrotas_contrincante=0
    )
    
    bonus_esperado = 5 + 5
    assert resultado.id_ganador == 1
    assert resultado.variacion_retador == 16 + bonus_esperado
    assert resultado.mensaje_personalizado == "¡De vuelta al juego! 🚀"
    print(f"Resultado: Retador gana {resultado.variacion_retador} puntos (16 base + {bonus_esperado} bonus). Mensaje: '{resultado.mensaje_personalizado}'")

def test_empate(db_session, usuario_base_retador, usuario_base_contrincante):
    """Prueba un escenario de empate."""
    print("\n--- Test: Empate ---")
    desempeno_retador = DesempenoJugador(id_usuario=1, respuestas_correctas=8, tiempo_total_seg=120)
    desempeno_contrincante = DesempenoJugador(id_usuario=2, respuestas_correctas=8, tiempo_total_seg=120)
    reto = RetoParaEvaluar(retador=desempeno_retador, contrincante=desempeno_contrincante)

    resultado = EvaluationChallengeService.procesar_evaluacion_reto(
        reto, usuario_base_retador, usuario_base_contrincante,
        racha_victorias_retador=0, racha_derrotas_retador=0,
        racha_victorias_contrincante=0, racha_derrotas_contrincante=0
    )
    
    assert resultado.id_ganador is None
    assert resultado.variacion_retador == 0
    assert resultado.mensaje_personalizado == "¡Empate! 🤝"
    print(f"Resultado: Empate. Sin cambios de puntos. Mensaje: '{resultado.mensaje_personalizado}'")

def test_victoria_foto_finish(db_session, usuario_base_retador, usuario_base_contrincante):
    """Prueba una victoria por una diferencia de rendimiento mínima."""
    print("\n--- Test: Foto Finish 📸 ---")
    desempeno_retador = DesempenoJugador(id_usuario=1, respuestas_correctas=5, tiempo_total_seg=100) # Puntuación: 5*10 - 100/100 = 49
    desempeno_contrincante = DesempenoJugador(id_usuario=2, respuestas_correctas=5, tiempo_total_seg=105) # Puntuación: 5*10 - 105/100 = 48.95
    reto = RetoParaEvaluar(retador=desempeno_retador, contrincante=desempeno_contrincante)
    
    resultado = EvaluationChallengeService.procesar_evaluacion_reto(
        reto, usuario_base_retador, usuario_base_contrincante,
        racha_victorias_retador=0, racha_derrotas_retador=0,
        racha_victorias_contrincante=0, racha_derrotas_contrincante=0
    )
    
    assert resultado.id_ganador == 1
    assert resultado.mensaje_personalizado == "¡Por un pelo! ¡Qué final tan reñido! 🤏"

def test_get_user_streak(db_session):
    """
    Prueba la función _get_user_streak para varios escenarios de rachas.
    """
    print("\n--- Inicio del Test: test_get_user_streak ---")

    # 1. Limpiar y preparar la base de datos
    print("\n[Paso 1] Limpiando la base de datos...")
    db_session.rollback()
    try:
        db_session.execute(text("TRUNCATE TABLE reto, juego, usuario, grado, tipo_texto, tematica, dificultad, escenario, tipo_juego, nivel, recompensa RESTART IDENTITY CASCADE"))
        db_session.commit()
        print(" -> Base de datos limpiada con éxito.")
    except Exception as e:
        print(f" -> Error truncando la base de datos: {e}")
        db_session.rollback()

    # 2. Crear datos de prueba base
    print("\n[Paso 2] Creando datos de prueba base (usuarios, grado, etc.)...")
    db_session.add(Grado(id_grado=1, nombre_grado="Primero", ciclo_grado=1, cantidad_usuarios=0))
    db_session.add(TipoTexto(id_tipo_texto=1, nombre_tipo_texto="Cuento"))
    db_session.add(Tematica(id_tematica=1, nombre_tematica="Aventura"))
    db_session.add(Dificultad(id_dificultad=1, nombre_dificultad="Fácil", valor_dificultad=1))
    db_session.add(Escenario(id_escenario=1, nombre_escenario="Bosque", niveles_requeridos=5))
    db_session.add(TipoJuego(id_tipo_juego=1, nombre_tipo_juego="Reto", descripcion="Duelo de conocimientos"))
    db_session.add(Nivel(id_nivel=1, nombre_nivel="Iniciado", descripcion_nivel="Primeros pasos"))
    db_session.add(Recompensa(id_recompensa=1, id_tipo_recompensa=1, cantidad=10))
    
    usuarios = [Usuario(id_usuario=i, student_id=f"student{i}", nombre_usuario=f"Test{i}", apellido_usuario=f"User{i}", email=f"test{i}@user.com", contrasena="pass") for i in range(1, 7)]
    db_session.add_all(usuarios)
    db_session.commit()
    print(" -> Datos base creados.")

    # 3. Crear juegos y retos para los escenarios
    print("\n[Paso 3] Simulando historial de juegos y retos...")
    
    # Escenario 1: Usuario 1 con racha de 3 victorias
    print(" -> Escenario 1: Usuario 1 debe tener racha de 3 victorias (V-V-V).")
    juego1 = Juego(nombre_juego=["Reto 1"], fecha_creacion=datetime(2025, 1, 1), id_tipo_juego=1, id_escenario=1, id_nivel=1, id_recompensa=1)
    juego2 = Juego(nombre_juego=["Reto 2"], fecha_creacion=datetime(2025, 1, 2), id_tipo_juego=1, id_escenario=1, id_nivel=1, id_recompensa=1)
    juego3 = Juego(nombre_juego=["Reto 3"], fecha_creacion=datetime(2025, 1, 3), id_tipo_juego=1, id_escenario=1, id_nivel=1, id_recompensa=1)
    db_session.add_all([juego1, juego2, juego3])
    db_session.commit()
    reto1 = Reto(id_juego=juego1.id_juego, id_usuario_retador=1, id_usuario_contrincante=2, ganador=1, estado="finalizado")
    reto2 = Reto(id_juego=juego2.id_juego, id_usuario_retador=1, id_usuario_contrincante=2, ganador=1, estado="finalizado")
    reto3 = Reto(id_juego=juego3.id_juego, id_usuario_retador=1, id_usuario_contrincante=2, ganador=1, estado="finalizado")

    # Escenario 2: Usuario 2 con racha de 4 derrotas
    print(" -> Escenario 2: Usuario 2 debe tener racha de 4 derrotas (D-D-D-D).")
    juego4 = Juego(nombre_juego=["Reto 4"], fecha_creacion=datetime(2025, 1, 4), id_tipo_juego=1, id_escenario=1, id_nivel=1, id_recompensa=1)
    db_session.add(juego4)
    db_session.commit()
    reto4 = Reto(id_juego=juego4.id_juego, id_usuario_retador=3, id_usuario_contrincante=2, ganador=3, estado="finalizado")

    # Escenario 3: Usuario 3 con racha rota (V, D, V -> racha actual de 1 victoria)
    print(" -> Escenario 3: Usuario 3 debe tener racha de 1 victoria (V-D-V).")
    juego5 = Juego(nombre_juego=["Reto 5"], fecha_creacion=datetime(2025, 1, 5), id_tipo_juego=1, id_escenario=1, id_nivel=1, id_recompensa=1)
    juego6 = Juego(nombre_juego=["Reto 6"], fecha_creacion=datetime(2025, 1, 6), id_tipo_juego=1, id_escenario=1, id_nivel=1, id_recompensa=1)
    juego_extra = Juego(nombre_juego=["Reto Extra"], fecha_creacion=datetime(2025, 1, 8), id_tipo_juego=1, id_escenario=1, id_nivel=1, id_recompensa=1)
    db_session.add_all([juego5, juego6, juego_extra])
    db_session.commit()
    reto5 = Reto(id_juego=juego5.id_juego, id_usuario_retador=3, id_usuario_contrincante=4, ganador=3, estado="finalizado")
    reto6 = Reto(id_juego=juego6.id_juego, id_usuario_retador=4, id_usuario_contrincante=3, ganador=4, estado="finalizado")
    reto_extra = Reto(id_juego=juego_extra.id_juego, id_usuario_retador=3, id_usuario_contrincante=4, ganador=3, estado="finalizado")

    # Escenario 5: Usuario 5 solo con empates
    print(" -> Escenario 4: Usuario 5 debe tener racha de 0 (solo empates).")
    juego7 = Juego(nombre_juego=["Reto 7"], fecha_creacion=datetime(2025, 1, 7), id_tipo_juego=1, id_escenario=1, id_nivel=1, id_recompensa=1)
    db_session.add(juego7)
    db_session.commit()
    reto7 = Reto(id_juego=juego7.id_juego, id_usuario_retador=5, id_usuario_contrincante=6, ganador=None, estado="finalizado")

    db_session.add_all([reto1, reto2, reto3, reto4, reto5, reto6, reto7, reto_extra])
    db_session.commit()
    print(" -> Historial de retos creado.")

    # 4. Llamar a la función y verificar
    print("\n[Paso 4] Verificando las rachas de cada usuario...")
    
    racha_u1 = EvaluationChallengeService._get_user_streak(1, db_session)
    print(f" -> Usuario 1: Racha esperada (3, 0), Racha obtenida {racha_u1}")
    assert racha_u1 == (3, 0), f"Error en Usuario 1. Esperado (3, 0), obtenido {racha_u1}"

    racha_u2 = EvaluationChallengeService._get_user_streak(2, db_session)
    print(f" -> Usuario 2: Racha esperada (0, 4), Racha obtenida {racha_u2}")
    assert racha_u2 == (0, 4), f"Error en Usuario 2. Esperado (0, 4), obtenido {racha_u2}"

    racha_u3 = EvaluationChallengeService._get_user_streak(3, db_session)
    print(f" -> Usuario 3: Racha esperada (1, 0), Racha obtenida {racha_u3}")
    assert racha_u3 == (1, 0), f"Error en Usuario 3. Esperado (1, 0), obtenido {racha_u3}"

    racha_u4 = EvaluationChallengeService._get_user_streak(4, db_session)
    print(f" -> Usuario 4: Racha esperada (0, 1), Racha obtenida {racha_u4}")
    assert racha_u4 == (0, 1), f"Error en Usuario 4. Esperado (0, 1), obtenido {racha_u4}"

    racha_u5 = EvaluationChallengeService._get_user_streak(5, db_session)
    print(f" -> Usuario 5: Racha esperada (0, 0), Racha obtenida {racha_u5}")
    assert racha_u5 == (0, 0), f"Error en Usuario 5. Esperado (0, 0), obtenido {racha_u5}"
    
    print(" -> Todas las verificaciones de rachas son correctas.")
    print("\n--- Fin del Test: test_get_user_streak ---")