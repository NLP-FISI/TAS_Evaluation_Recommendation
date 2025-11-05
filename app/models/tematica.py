# app/models/tematica.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base
from .usuario import usuario_preferencia_table


class Tematica(Base):
    __tablename__ = 'tematica'

    id_tematica = Column(Integer, primary_key=True, index=True)
    nombre_tematica = Column(String(50), unique=True, nullable=False)

    # Relación inversa para saber qué usuarios tienen esta temática
    usuarios = relationship(
        "Usuario",
        secondary=usuario_preferencia_table,
        back_populates="preferencias"
    )
