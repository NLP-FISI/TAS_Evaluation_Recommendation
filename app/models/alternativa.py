"""Modelo para alternativas de respuesta"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Alternativa(Base):
    __tablename__ = 'alternativa'
    
    id_alternativa = Column(Integer, primary_key=True, index=True)
    id_pregunta = Column(Integer, ForeignKey('pregunta.id_pregunta'), nullable=False)
    contenido = Column(String(100), nullable=False)
    correcto = Column(Boolean, nullable=False, default=False)

    pregunta = relationship("Pregunta", back_populates="alternativas")
    resultados = relationship("ResultadoDiagnostico", back_populates="alternativa_elegida")
