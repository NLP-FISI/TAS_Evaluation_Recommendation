# app/models/tematica.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Tematica(Base):
    """
    Modelo SQLAlchemy que representa la tabla 'tematica'.
    """
    __tablename__ = 'tematica'

    id_tematica = Column(Integer, primary_key=True, index=True)
    nombre_tematica = Column(String(50), unique=True, nullable=False)

    # Relación directa con Usuario a través de la tabla de asociación
    usuarios = relationship(
        "Usuario",
        secondary="usuario_preferencia",  # referencia al nombre de tabla
        back_populates="preferencias"
    )

    # Relación con la clase de asociación (opcional pero recomendable)
    usuario_preferencias = relationship(
        "UsuarioPreferencia",
        back_populates="tematica"
    )
