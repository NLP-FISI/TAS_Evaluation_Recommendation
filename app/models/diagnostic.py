"""
Modelos SQLAlchemy para las entidades relacionadas con el diagnóstico.
Incluye Texto, Pregunta, Alternativa y ResultadoDiagnostico.
"""
from sqlalchemy import (Column, Integer, String, Boolean, DateTime,
                        ForeignKey, Table, Text, Enum as SQLEnum)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
import enum
import logging # Importar logging para advertencias

# Usamos la Base declarada en database.py si existe, o creamos una local
try:
    from app.core.database import Base
except ImportError:
    logging.warning("app.core.database.Base no encontrada. Usando declarative_base local.")
    Base = declarative_base()

# Aseguramos que los modelos Usuario y Tematica estén disponibles desde user_profile
try:
    from .user_profile import Usuario, Tematica
except ImportError:
    # SI ESTE ERROR OCURRE, ALGO ESTÁ MAL CON LA ESTRUCTURA O user_profile.py
    logging.error("No se pudieron importar Usuario y Tematica desde .user_profile. Asegúrate que app/models/user_profile.py exista y sea correcto.")
    # NO REDEFINIMOS LAS CLASES AQUÍ PARA EVITAR ERRORES DE DUPLICADOS
    # Si la importación falla, la aplicación probablemente no funcionará correctamente,
    # pero al menos no tendremos el error de definición duplicada al iniciar.
    # Necesitaríamos arreglar la causa raíz de por qué no se puede importar.
    # Temporalmente, podríamos poner placeholders si fuera estrictamente necesario,
    # pero es mejor arreglar la importación.
    # class Usuario(Base): pass # Placeholder - NO RECOMENDADO
    # class Tematica(Base): pass # Placeholder - NO RECOMENDADO
    raise # Relanzamos el error de importación para saber que algo falló


# --- Tablas de soporte (si no existen ya en otro modelo) ---

class TipoTexto(Base):
    __tablename__ = 'tipo_texto'
    id_tipo_texto = Column(Integer, primary_key=True, index=True)
    nombre_tipo_texto = Column(String(50), nullable=False, unique=True)
    textos = relationship("Texto", back_populates="tipo_texto")

class Dificultad(Base):
    __tablename__ = 'dificultad'
    id_dificultad = Column(Integer, primary_key=True, index=True)
    nombre_dificultad = Column(String(50), nullable=False, unique=True)
    valor_dificultad = Column(Integer)
    textos = relationship("Texto", back_populates="dificultad")
    preguntas = relationship("Pregunta", back_populates="dificultad")

class TipoPregunta(Base):
    __tablename__ = 'tipo_pregunta'
    id_tipo_pregunta = Column(Integer, primary_key=True, index=True)
    nombre_tipo_pregunta = Column(String(50), nullable=False, unique=True) # e.g., 'literal', 'inferencial', 'critico'
    preguntas = relationship("Pregunta", back_populates="tipo_pregunta")


# --- Modelos Principales para Diagnóstico ---

class Texto(Base):
    __tablename__ = 'texto'
    id_texto = Column(Integer, primary_key=True, index=True)
    id_tipo_texto = Column(Integer, ForeignKey('tipo_texto.id_tipo_texto'))
    id_dificultad = Column(Integer, ForeignKey('dificultad.id_dificultad'))
    id_tematica = Column(Integer, ForeignKey('tematica.id_tematica')) # Ahora usa la Tematica importada
    titulo = Column(String(100))
    contenido = Column(Text, nullable=False)

    tipo_texto = relationship("TipoTexto", back_populates="textos")
    dificultad = relationship("Dificultad", back_populates="textos")
    # Asegúrate que la relación inversa exista en user_profile.py si usas preferencias
    tematica = relationship("Tematica") # Relación simple si no necesitas back_populates aquí
    preguntas = relationship("Pregunta", back_populates="texto")

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
