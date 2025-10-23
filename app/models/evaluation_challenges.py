# File: app/models/evaluation_challenges.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON
from sqlalchemy.sql import func
from app.core.database import Base

class Usuario(Base):
    """
    Modelo de SQLAlchemy que se mapea a la tabla 'usuario' en la base de datos.
    """
    __tablename__ = 'usuario'
    
    # Mapeo de columnas según tu script de base de datos
    id_usuario = Column(Integer, primary_key=True, index=True)
    id_grado = Column(Integer) 
    nombre_usuario = Column(String(50), nullable=False)
    apellido_usuario = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    
    # La columna 'puntos' almacenará el puntaje ELO
    puntos = Column(Integer, default=1500) # Un ELO inicial común es 1500