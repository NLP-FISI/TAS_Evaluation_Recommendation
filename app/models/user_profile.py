from sqlalchemy import (Column, Integer, String, Boolean, DateTime, 
                        ForeignKey, Table, JSON)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

# Tabla de unión para la relación muchos a muchos entre Usuario y Tematica
usuario_preferencia_table = Table('usuario_preferencia', Base.metadata,
    Column('usuario_id', Integer, ForeignKey('usuario.id_usuario'), primary_key=True),
    Column('tematica_id', Integer, ForeignKey('tematica.id_tematica'), primary_key=True)
)

class Usuario(Base):
    __tablename__ = 'usuario'

    id_usuario = Column(Integer, primary_key=True, index=True)
    id_grado = Column(Integer, ForeignKey('grado.id_grado'))
    nombre_usuario = Column(String(50))
    apellido_usuario = Column(String(50))
    email = Column(String(50), unique=True, index=True)
    # ... otros campos de tu tabla Usuario ...
    
    # Campo para guardar la configuración del avatar como un JSON
    configuracion_avatar = Column(JSON)

    # Relación con la tabla Grado
    grado = relationship("Grado")
    
    # Relación muchos a muchos con la tabla Tematica
    preferencias = relationship(
        "Tematica",
        secondary=usuario_preferencia_table,
        back_populates="usuarios"
    )

class Grado(Base):
    __tablename__ = 'grado'

    id_grado = Column(Integer, primary_key=True, index=True)
    nombre_grado = Column(String(50))
    # ... otros campos ...

class Tematica(Base):
    __tablename__ = 'tematica'

    id_tematica = Column(Integer, primary_key=True, index=True)
    nombre_tematica = Column(String(50))

    # Relación inversa para saber qué usuarios tienen esta temática
    usuarios = relationship(
        "Usuario",
        secondary=usuario_preferencia_table,
        back_populates="preferencias"
    )
