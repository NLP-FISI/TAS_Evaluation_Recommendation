"""
Modelos SQLAlchemy para las entidades relacionadas con el diagnóstico.
Incluye Texto, Pregunta, Alternativa y ResultadoDiagnostico.
"""
from sqlalchemy import (Column, Integer, String, Boolean, DateTime,
                        ForeignKey, Table, Text, Enum as SQLEnum)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
from app.models.tipo_texto import TipoTexto
import enum
import logging # Importar logging para advertencias

# Usamos la Base declarada en database.py si existe, o creamos una local
try:
    from app.core.database import Base
except ImportError:
    logging.warning("app.core.database.Base no encontrada. Usando declarative_base local.")
    Base = declarative_base()

# Aseguramos que los modelos Usuario y Tematica estén disponibles desde archivos separados
try:
    from .usuario import Usuario
    from .tematica import Tematica
except ImportError:
    # SI ESTE ERROR OCURRE, ALGO ESTÁ MAL CON LA ESTRUCTURA
    logging.error("No se pudieron importar Usuario desde .usuario o Tematica desde .tematica.")
    raise # Relanzamos el error de importación para saber que algo falló


# --- Tablas de soporte (si no existen ya en otro modelo) ---
class TipoPregunta(Base):
    __tablename__ = 'tipo_pregunta'
    id_tipo_pregunta = Column(Integer, primary_key=True, index=True)
    nombre_tipo_pregunta = Column(String(50), nullable=False, unique=True) # e.g., 'literal', 'inferencial', 'critico'
    preguntas = relationship("Pregunta", back_populates="tipo_pregunta")


# --- Modelos Principales para Diagnóstico ---

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

class Alternativa(Base):
    __tablename__ = 'alternativa'
    id_alternativa = Column(Integer, primary_key=True, index=True)
    id_pregunta = Column(Integer, ForeignKey('pregunta.id_pregunta'), nullable=False)
    contenido = Column(String(100), nullable=False)
    correcto = Column(Boolean, nullable=False, default=False)

    pregunta = relationship("Pregunta", back_populates="alternativas")
    resultados = relationship("ResultadoDiagnostico", back_populates="alternativa_elegida")


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
