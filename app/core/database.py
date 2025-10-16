# File: app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Crea la URL de la base de datos usando la configuración importada
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Crea el motor de SQLAlchemy
# El argumento connect_args es específico para SQLite, se puede omitir para PostgreSQL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Crea una clase SessionLocal, que será la fábrica de sesiones de la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crea una clase Base que servirá como la clase base para todos los modelos de la aplicación
Base = declarative_base()

# --- Función de Dependencia para los Endpoints ---
def get_db():
    """
    Esta función es una dependencia de FastAPI que crea una nueva sesión
    de base de datos para cada solicitud y la cierra cuando termina.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()