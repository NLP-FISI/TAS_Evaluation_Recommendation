"""Modelo para tipos de pregunta (literal, inferencial, crítico)"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class TipoPregunta(Base):
    __tablename__ = 'tipo_pregunta'
    
    id_tipo_pregunta = Column(Integer, primary_key=True, index=True)
    nombre_tipo_pregunta = Column(String(50), nullable=False, unique=True)
    
    preguntas = relationship("Pregunta", back_populates="tipo_pregunta")
