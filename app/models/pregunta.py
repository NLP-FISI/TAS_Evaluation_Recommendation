"""Modelo para preguntas de comprensión lectora"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Pregunta(Base):
    __tablename__ = 'pregunta'
    
    id_pregunta = Column(Integer, primary_key=True, index=True)
    id_texto = Column(Integer, ForeignKey('texto.id_texto'), nullable=False)
    id_tipo_pregunta = Column(Integer, ForeignKey('tipo_pregunta.id_tipo_pregunta'), nullable=False)
    id_dificultad = Column(Integer, ForeignKey('dificultad.id_dificultad'), nullable=False)
    contenido = Column(String(100), nullable=False)

    texto = relationship("Texto", back_populates="preguntas")
    tipo_pregunta = relationship("TipoPregunta", back_populates="preguntas")
    dificultad = relationship("Dificultad", back_populates="preguntas")
    alternativas = relationship("Alternativa", back_populates="pregunta", cascade="all, delete-orphan")
    resultados = relationship("ResultadoDiagnostico", back_populates="pregunta")
