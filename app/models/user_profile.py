# app/models/user_profile.py
from sqlalchemy import (Column, Integer, String, Boolean, DateTime, 
                        ForeignKey, Table, JSON)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

# Usamos la Base declarada en database.py para que todos los modelos la compartan
from app.core.database import Base

# Tabla de unión para la relación muchos a muchos entre Usuario y Tematica
# Define la tabla que conecta a los usuarios con sus preferencias.
usuario_preferencia_table = Table('usuario_preferencia', Base.metadata,
    Column('usuario_id', Integer, ForeignKey('usuario.id_usuario'), primary_key=True),
    Column('tematica_id', Integer, ForeignKey('tematica.id_tematica'), primary_key=True)
)

class Usuario(Base):
    """
    Modelo SQLAlchemy que representa la tabla 'usuario'.
    """
    __tablename__ = 'usuario'

    # Columnas de la tabla
    id_usuario = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(100), unique=True, index=True, nullable=False) # Columna clave para F-01
    id_grado = Column(Integer, ForeignKey('grado.id_grado'))
    nombre_usuario = Column(String(50), nullable=False) # Requerido por la base de datos
    apellido_usuario = Column(String(50), nullable=False) # Requerido por la base de datos
    contrasena = Column(String(255), nullable=False) # Requerido por la base de datos
    email = Column(String(50), unique=True, index=True, nullable=True)
    
    # Columna para guardar la configuración del avatar como un JSON
    configuracion_avatar = Column(JSON)

    # Relaciones con otras tablas
    grado = relationship("Grado")
    
    # Relación muchos a muchos con la tabla Tematica a través de la tabla de unión
    preferencias = relationship(
        "Tematica",
        secondary=usuario_preferencia_table,
        back_populates="usuarios"
    )

class Grado(Base):
    """
    Modelo SQLAlchemy que representa la tabla 'grado'.
    """
    __tablename__ = 'grado'

    id_grado = Column(Integer, primary_key=True, index=True)
    nombre_grado = Column(String(50), nullable=False)
    ciclo_grado = Column(Integer, nullable=False)

class Tematica(Base):
    """
    Modelo SQLAlchemy que representa la tabla 'tematica'.
    """
    __tablename__ = 'tematica'

    id_tematica = Column(Integer, primary_key=True, index=True)
    nombre_tematica = Column(String(50), unique=True, nullable=False)

    # Relación inversa para saber qué usuarios tienen esta temática
    usuarios = relationship(
        "Usuario",
        secondary=usuario_preferencia_table,
        back_populates="preferencias"
    )

