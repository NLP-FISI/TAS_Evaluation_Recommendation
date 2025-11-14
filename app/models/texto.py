"""Modelo para textos de lectura"""

from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class Texto(Base):
    """
    Representa un texto de lectura asociado a un tipo, dificultad y temática.
    """
    __tablename__ = 'texto'
    
    id_texto = Column(Integer, primary_key=True, index=True)
    id_tipo_texto = Column(Integer, ForeignKey('tipo_texto.id_tipo_texto'))
    id_dificultad = Column(Integer, ForeignKey('dificultad.id_dificultad'))
    id_tematica = Column(Integer, ForeignKey('tematica.id_tematica'))

    titulo = Column(String(100))
    contenido = Column(Text, nullable=False)

    # Relaciones principales
    tipo_texto = relationship("TipoTexto", back_populates="textos")
    dificultad = relationship("Dificultad", back_populates="textos")
    tematica = relationship("Tematica")

    # Relaciones inversas
    preguntas = relationship("Pregunta", back_populates="texto")
    resultado_texto = relationship("ResultadoTexto", back_populates="texto")
