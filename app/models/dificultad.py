"""Modelo para niveles de dificultad"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Dificultad(Base):
    __tablename__ = 'dificultad'
    
    id_dificultad = Column(Integer, primary_key=True, index=True)
    nombre_dificultad = Column(String(50), nullable=False, unique=True)
    valor_dificultad = Column(Integer)
    
    textos = relationship("Texto", back_populates="dificultad")
    preguntas = relationship("Pregunta", back_populates="dificultad")
