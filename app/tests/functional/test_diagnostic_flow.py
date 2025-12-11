import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from app.main import app 

# --- Importamos Modelos para preparar la "Cancha" (BD) ---
from app.models.usuario import Usuario
from app.models.grado import Grado
from app.models.tematica import Tematica
from app.models.texto import Texto
from app.models.pregunta import Pregunta
from app.models.alternativa import Alternativa
from app.models.tipo_pregunta import TipoPregunta
from app.models.tipo_texto import TipoTexto
from app.models.dificultad import Dificultad
# Importamos modelos para limpiar
from app.models.resultado_diagnostico import ResultadoDiagnostico
from app.models.desempenio import Desempenio

@pytest.fixture
def client():
    """Cliente para hacer peticiones HTTP a la API"""
    return TestClient(app)

@pytest.fixture
def setup_diagnostic_data(db_session):
    """
    Prepara todo el escenario: Limpia tablas y crea las Preguntas/Alternativas
    necesarias para que el Diagnóstico funcione (IDs 1 a 5).
    """
    # 1. LIMPIEZA PROFUNDA (Copiada de tu éxito en integración)
    db_session.execute(text("TRUNCATE TABLE resultado_diagnostico, desempenio, alternativa, pregunta, texto, usuario RESTART IDENTITY CASCADE;"))
    
    # 2. CREAR DATOS MAESTROS (Dependencias de Claves Foráneas)
    grado = Grado(id_grado=4, nombre_grado="4to", ciclo_grado=1)
    tematica = Tematica(id_tematica=1, nombre_tematica="General")
    dificultad = Dificultad(id_dificultad=1, nombre_dificultad="Media", valor_dificultad=1)
    tipo_p = TipoPregunta(id_tipo_pregunta=1, nombre_tipo_pregunta="Literal")
    tipo_t = TipoTexto(id_tipo_texto=1, nombre_tipo_texto="Cuento")
    
    db_session.add_all([grado, tematica, dificultad, tipo_p, tipo_t])
    db_session.commit()

    # 3. CREAR TEXTO (Padre de las preguntas)
    texto = Texto(id_texto=1, id_tipo_texto=1, id_dificultad=1, id_tematica=1, titulo="T", contenido="C")
    db_session.add(texto)
    db_session.commit()

    # 4. CREAR PREGUNTAS (IDs 1 y 2 para Etapa 1 -- IDs 3,4,5 para Etapa 2)
    # Requerido por: STAGE_1_QUESTIONS y STAGE_2_QUESTIONS en el servicio
    preguntas = []
    for i in range(1, 6): # IDs 1 al 5
        p = Pregunta(id_pregunta=i, id_texto=1, id_tipo_pregunta=1, id_dificultad=1, contenido=f"Pregunta {i}?")
        preguntas.append(p)
    db_session.add_all(preguntas)
    db_session.commit()

    # 5. CREAR ALTERNATIVAS (Una correcta y una incorrecta por pregunta)
    alternativas = []
    for i in range(1, 6):
        # Alt Correcta (ID = i*10 + 1) -> Ej: 11, 21, 31...
        alternativas.append(Alternativa(id_alternativa=i*10+1, id_pregunta=i, contenido="Correcta", correcto=True))
        # Alt Incorrecta (ID = i*10 + 2) -> Ej: 12, 22, 32...
        alternativas.append(Alternativa(id_alternativa=i*10+2, id_pregunta=i, contenido="Incorrecta", correcto=False))
    
    db_session.add_all(alternativas)
    
    # 6. CREAR USUARIO DE PRUEBA
    user = Usuario(
        student_id="DIAG-TEST", 
        nombre_usuario="Tester", 
        apellido_usuario="QA", 
        email="qa@test.com", 
        contrasena="123", 
        id_grado=4
    )
    db_session.add(user)
    db_session.commit()
    
    return "DIAG-TEST"

# --- TESTS FUNCIONALES (El "User Journey") ---

def test_diagnostic_full_flow_success(client, setup_diagnostic_data):
    """
    Prueba el "Camino Feliz": 
    1. Usuario responde bien Etapa 1 -> Sistema dice CONTINUAR.
    2. Usuario responde bien Etapa 2.
    3. Sistema asigna nivel alto.
    """
    student_id = setup_diagnostic_data
    
    # --- PASO 1: Responder Etapa 1 (Preguntas 1 y 2) ---
    # Enviamos las alternativas correctas (11 y 21)
    payload_stage1 = {
        "student_id": student_id,
        "answers": [
            {"question_id": 1, "alternative_id": 11},
            {"question_id": 2, "alternative_id": 21}
        ]
    }
    
    response1 = client.post("/api/v1/diagnostic/stage1", json=payload_stage1)
    assert response1.status_code == 200
    data1 = response1.json()
    assert data1["decision"] == "CONTINUAR", "Debería pasar a la siguiente etapa con 2 aciertos."
    assert data1["correct_answers_count"] == 2

    # --- PASO 2: Responder Etapa 2 (Preguntas 3, 4 y 5) ---
    # Enviamos correctas (31, 41, 51)
    payload_stage2 = {
        "student_id": student_id,
        "answers": [
            {"question_id": 3, "alternative_id": 31},
            {"question_id": 4, "alternative_id": 41},
            {"question_id": 5, "alternative_id": 51}
        ]
    }
    
    response2 = client.post("/api/v1/diagnostic/stage2", json=payload_stage2)
    assert response2.status_code == 200
    data2 = response2.json()
    assert data2["correct_answers_count"] == 3

    # --- PASO 3: Asignación de Nivel (Cálculo Final) ---
    payload_assign = {"student_id": student_id}
    response3 = client.post("/api/v1/diagnostic/assign-level", json=payload_assign)
    
    assert response3.status_code == 200
    data3 = response3.json()
    
    # Con 5/5 aciertos, la lógica (F-03) debería asignar el grado máximo posible
    assert "6to Grado" in data3["assigned_level_label"]
    print(f"\n[QA] Flujo completado. Nivel asignado: {data3['assigned_level_label']}")

def test_diagnostic_fail_early(client, setup_diagnostic_data):
    """
    Prueba el "Camino de Fallo":
    1. Usuario falla Etapa 1 -> Sistema dice FINALIZAR.
    """
    student_id = setup_diagnostic_data
    
    # Enviamos respuestas incorrectas (12 y 22)
    payload_fail = {
        "student_id": student_id,
        "answers": [
            {"question_id": 1, "alternative_id": 12},
            {"question_id": 2, "alternative_id": 22}
        ]
    }
    
    response = client.post("/api/v1/diagnostic/stage1", json=payload_fail)
    assert response.status_code == 200
    data = response.json()
    
    assert data["decision"] == "FINALIZAR", "Debería terminar el examen con 0 aciertos."
    assert data["correct_answers_count"] == 0