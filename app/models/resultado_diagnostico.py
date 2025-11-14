"""Modelo para almacenar resultados del diagnóstico inicial"""
from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class ResultadoDiagnostico(Base):
    __tablename__ = 'resultado_diagnostico'
    
    id_resultado_diagnostico = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'), nullable=False, index=True)
    id_pregunta = Column(Integer, ForeignKey('pregunta.id_pregunta'), nullable=False, index=True)
    id_alternativa_elegida = Column(Integer, ForeignKey('alternativa.id_alternativa'), nullable=False)
    es_correcta = Column(Boolean, nullable=False)
    fecha_respuesta = Column(DateTime(timezone=True), server_default=func.now())

    usuario = relationship("Usuario")
    pregunta = relationship("Pregunta", back_populates="resultados")
    alternativa_elegida = relationship("Alternativa", back_populates="resultados")
