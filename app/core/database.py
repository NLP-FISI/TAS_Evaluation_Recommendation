# Este archivo contendrá la configuración de la conexión a la base de datos.
# Usaremos SQLAlchemy, el ORM estándar en el ecosistema de FastAPI.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# --- 1. CONFIGURACIÓN DE LA CONEXIÓN ---
# Esta es la URL de conexión a tu base de datos en la nube.
# La obtendrás de tu proveedor (ej. ElephantSQL, Aiven, AWS RDS).
# Ejemplo para PostgreSQL:
# DATABASE_URL = "postgresql://user:password@host:port/database"

# Para desarrollo y pruebas, es muy común usar una base de datos SQLite local.
# Es un simple archivo en tu disco.
SQLALCHEMY_DATABASE_URL = "sqlite:///./tas_database.db"

# --- 2. CREACIÓN DEL "MOTOR" DE LA BASE DE DATOS ---
# El 'engine' es el punto de entrada a la base de datos.
# El argumento connect_args es solo necesario para SQLite para permitir multithreading.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# --- 3. CREACIÓN DE LA SESIÓN ---
# Cada instancia de SessionLocal será una sesión de base de datos.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- 4. MODELO BASE ---
# Crearemos una clase Base. Nuestros modelos de ORM (ej. la clase Usuario)
# heredarán de esta clase.
Base = declarative_base()


# ==============================================================================
# == FUNCIÓN DE DEPENDENCIA (ESTA ES LA PARTE QUE FALTA) ==
# ==============================================================================
def get_db():
    """
    Dependencia de FastAPI para obtener una sesión de base de datos.
    - Se crea una sesión (db) para cada petición.
    - Se entrega la sesión a la función del endpoint (`yield db`).
    - Al final de la petición, se cierra la sesión (`db.close()`).
    Esto asegura que las sesiones de base de datos se abran y cierren correctamente.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()