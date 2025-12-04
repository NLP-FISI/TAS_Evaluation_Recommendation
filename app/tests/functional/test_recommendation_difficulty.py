import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from app.main import app 
from app.models.usuario import Usuario
from app.models.juego import Juego
from app.models.texto import Texto
from app.models.resultado_juego import ResultadoJuego
from app.models.resultado_texto import ResultadoTexto
from app.models.dificultad import Dificultad
from app.models.grado import Grado
from app.schemas.recommendation_schemas import UpdateDifficultyRequest


# Fixture para el cliente de prueba de FastAPI
@pytest.fixture(scope="module")
def client():
    """Provee un cliente de prueba para la aplicación FastAPI."""
    with TestClient(app) as c:
        yield c

# ----------------------------------------------------------------------
# --- Fixture de Limpieza y Setup de Datos ---
# ----------------------------------------------------------------------

@pytest.fixture
def setup_irt_data(db_session):
    """
    Prepara la BD con un usuario, un juego y los resultados necesarios
    para que la lógica de dificultad funcione.
    """
    # 1. Limpieza Mínima de Tablas Críticas (Para evitar errores de FK)
    # Ya que pausamos la limpieza profunda, limpiamos solo las tablas directas.
    db_session.query(ResultadoTexto).delete()
    db_session.query(ResultadoJuego).delete()
    db_session.query(Usuario).delete()
    db_session.query(Grado).delete()
    db_session.query(Dificultad).delete()
    db_session.commit()

    # 2. Creación de Datos Catálogo y Base
    db_session.add(Dificultad(id_dificultad=1, nombre_dificultad="Fácil", valor_dificultad=1))
    db_session.add(Dificultad(id_dificultad=3, nombre_dificultad="Medio", valor_dificultad=3))
    db_session.add(Dificultad(id_dificultad=5, nombre_dificultad="Difícil", valor_dificultad=5))
    db_session.add(Grado(id_grado=3, nombre_grado="3er Grado", ciclo_grado=1))
    
    # Usuario Inicial: Habilidad Acumulada = 2.0 (Theta)
    user = Usuario(
        id_usuario=1, 
        student_id="IRT-001", 
        nombre_usuario="TestIRT", 
        apellido_usuario="User",
        email="irt@test.com", 
        contrasena="pass", 
        id_grado=3,
        dificultad_acumulada=2.0 
    )
    db_session.add(user)

    # Juego
    juego = Juego(id_juego=10, nombre_juego=["Juego Test Dificultad"])
    db_session.add(juego)

    # Textos: 3 textos con dificultad promedio de 3.0 (Beta)
    texto1 = Texto(id_texto=101, id_dificultad=3, titulo="T1", contenido="c1")
    texto2 = Texto(id_texto=102, id_dificultad=3, titulo="T2", contenido="c2")
    db_session.add_all([texto1, texto2])

    # Resultados de Juego: 6 Correctas, 2 Incorrectas -> Resultado GENERAL: 1 (Victoria)
    res_juego = ResultadoJuego(
        id_resultado_juego=20, 
        id_juego=10, 
        id_usuario=1, 
        correctas=6, 
        incorrectas=2
    )
    db_session.add(res_juego)

    # Resultados de Texto (Asocia textos al juego)
    res_t1 = ResultadoTexto(id_resultado_texto=301, id_texto=101, id_juego=10, id_usuario=1)
    res_t2 = ResultadoTexto(id_resultado_texto=302, id_texto=102, id_juego=10, id_usuario=1)
    db_session.add_all([res_t1, res_t2])

    db_session.commit()
    return {"id_usuario": user.id_usuario, "id_juego": juego.id_juego}


# ----------------------------------------------------------------------
# --- Casos de Prueba Funcional (Llamada al Endpoint) ---
# ----------------------------------------------------------------------

def test_functional_difficulty_update_success(client, setup_irt_data, db_session):
    """
    Valida el flujo funcional completo: llama a la API, actualiza el usuario en la BD,
    y verifica el resultado de la recomendación IRT.
    """
    id_usuario = setup_irt_data["id_usuario"]
    id_juego = setup_irt_data["id_juego"]
    
    # 1. ACT: Llamar al Endpoint de FastAPI
    response = client.post(
        "/api/v1/recommendation/difficulty/update",
        json={"id_usuario": id_usuario, "id_juego": id_juego}
    )
    
    # 2. ASSERT DE LA RESPUESTA DE LA API (HTTP Code y Estructura)
    assert response.status_code == 200, f"Error de API: {response.text}"
    data = response.json()
    
    # Verificación de datos críticos en la respuesta
    assert data["id_usuario"] == id_usuario
    assert data["dificultad_acumulada_anterior"] == 2.0
    assert data["promedio_dificultad_juego"] == 3.0 # Promedio de (3+3)/2
    assert data["recomendacion_de_dificultad"] in [2, 3], "La recomendación (Beta) no está en el rango esperado."
    
    # 3. ASSERT DE LA INTEGRACIÓN (Verificar la DB)
    # Re-consultar al usuario para ver el cambio de estado (persistencia)
    db_user_updated = db_session.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    
    # El usuario ganó (Resultado=1) y su theta (2.0) era menor a Beta (3.0), por lo que debe SUBIR.
    assert db_user_updated.dificultad_acumulada > 2.0, "La dificultad acumulada no se actualizó en la BD."