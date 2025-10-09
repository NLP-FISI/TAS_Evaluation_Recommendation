# app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexión (ajústala a tu base real)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
# Ejemplo si usas Postgres:
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={
        "check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 🔹 Esta función es la que te falta


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
