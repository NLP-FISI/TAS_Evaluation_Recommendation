# Framework principal

pip install fastapi

# Servidor ASGI para ejecutar FastAPI

pip install uvicorn[standard]

# ORM para base de datos relacional (PostgreSQL recomendado)

pip install sqlalchemy

# Driver para PostgreSQL (puede cambiar si usan otra BD)

pip install psycopg2-binary

# Migraciones de BD

pip install alembic

# Validación y serialización (FastAPI ya usa Pydantic, pero mejor instalar explícitamente)

pip install pydantic

# Variables de entorno (para configuración segura)

pip install python-dotenv

# Testing

pip install pytest
pip install httpx    # Para testear endpoints de FastAPI
