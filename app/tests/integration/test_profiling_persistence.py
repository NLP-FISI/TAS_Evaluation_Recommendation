import pytest
from sqlalchemy import text 

# --- Importaciones de Servicios y Esquemas ---
from app.services.profiling_service import ProfilingService
from app.schemas.profiling_schemas import ProfilingRequest

# --- Importaciones de Modelos (para la limpieza en cascada ORM) ---
from app.models.grado import Grado
from app.models.tematica import Tematica
from app.models.usuario import Usuario
from app.models.usuario_preferencia import UsuarioPreferencia
from app.models.desempenio import Desempenio 
from app.models.resultado_diagnostico import ResultadoDiagnostico 
from app.models.resultado_texto import ResultadoTexto 
from app.models.resultado_juego import ResultadoJuego 
from app.models.reto import Reto 
from app.models.experience_level import ExperienceLevel 
# NO importamos RespuestaUsuario porque causa el error UndefinedTable.


@pytest.fixture
def setup_db_for_profiling(db_session):
    """
    Fixture que ejecuta una limpieza profunda y definitiva (Deep Clean) 
    de todas las tablas que referencian a 'usuario' en orden de dependencia.
    """
    
    # 1. LIMPIEZA DE TABLAS DEPENDIENTES (ORM)
    
    # --- Manejo del error UndefinedTable para 'respuesta_usuario' ---
    try:
        # Intentamos borrar con SQL plano la tabla que nos está dando problemas.
        # Si no existe, el 'except' lo captura y permite continuar.
        db_session.execute(text("DELETE FROM respuesta_usuario;"))
    except Exception:
        pass # Ignoramos el error UndefinedTable y continuamos.
    # -----------------------------------------------------------------

    db_session.query(ResultadoDiagnostico).delete() 
    db_session.query(ResultadoTexto).delete()       
    db_session.query(ResultadoJuego).delete()       
    db_session.query(Reto).delete()
    db_session.query(Desempenio).delete()
    db_session.query(UsuarioPreferencia).delete()
    db_session.query(ExperienceLevel).delete()

    
    # 2. LIMPIEZA DE TABLAS DE ASOCIACIÓN (SQL PLANO)
    # Tablas que causaron ForeignKeyViolation anteriormente.
    db_session.execute(text("DELETE FROM amigos;"))
    db_session.execute(text("DELETE FROM usuario_logro;"))
    db_session.execute(text("DELETE FROM usuario_nivel;"))
    db_session.execute(text("DELETE FROM ranking;"))

    
    # 3. LIMPIEZA DE TABLAS PRINCIPALES Y CATÁLOGOS
    db_session.query(Usuario).delete()
    db_session.query(Grado).delete()
    db_session.query(Tematica).delete()
    db_session.commit()

    # 4. SETUP: Crear datos base para la prueba
    db_session.add_all([
        Grado(id_grado=2, nombre_grado="2do Grado", ciclo_grado=1),
        Grado(id_grado=3, nombre_grado="3er Grado", ciclo_grado=1),
    ])
    
    db_session.add_all([
        Tematica(id_tematica=1, nombre_tematica="Animales"),
        Tematica(id_tematica=3, nombre_tematica="Ciencia")
    ])
    
    db_session.commit()

# --- La función de prueba (no necesita cambios) ---

def test_create_new_user_profile_persistence(db_session, setup_db_for_profiling):
    """
    Certifica que el servicio ProfilingService cree correctamente el usuario
    y persista su grado y preferencias en la Base de Datos.
    """
    student_id = "STU-001"
    grade_level = 3
    preferences = [1, 3] 
    
    request_data = ProfilingRequest(
        student_id=student_id,
        grade_level=grade_level,
        preferences=preferences
    )
    
    # ACT: Llamar al servicio de negocio
    response = ProfilingService.create_profile(request_data, db_session)
    
    # ASSERT 1: Validación de la respuesta del servicio
    assert response.profile_created is True
    
    # ASSERT 2: Validación de la Persistencia en la BD
    db_user = db_session.query(Usuario).filter(Usuario.student_id == student_id).first()
    
    assert db_user is not None
    assert db_user.id_grado == grade_level
    assert len(db_user.preferencias) == 2
    
    saved_pref_ids = sorted([p.id_tematica for p in db_user.preferencias])
    assert saved_pref_ids == preferences