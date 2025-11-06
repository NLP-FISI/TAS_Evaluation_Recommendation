# File: app/test/conftest.py
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# --- Configuración Clave ---
# Carga las variables del entorno de prueba ANTES de que la app las cargue.
# Esto asegura que SQLAlchemy use la base de datos de prueba.
print("Cargando entorno desde .env.test")
load_dotenv(dotenv_path=".env.test")

# Re-importar settings DESPUÉS de cargar el .env.test
from app.core.config import settings
from app.models import usuario # Asegúrate de que los modelos se carguen

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear todas las tablas si no existen (útil para la primera ejecución)
# En un entorno CI/CD real, esto se manejaría de forma más robusta.
usuario.Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """
    1. Inicia una conexión y una transacción.
    2. "yield" (entrega) la sesión a la función de prueba que la solicita.
    3. Cuando la prueba termina, el código continúa y ejecuta el "rollback".

    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()