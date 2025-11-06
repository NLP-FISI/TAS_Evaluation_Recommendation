"""Modelo para tipos de texto (narrativo, expositivo, argumentativo, etc.)"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class TipoTexto(Base):
    """
    Representa los diferentes tipos de texto posibles (narrativo, expositivo, argumentativo, etc.).
    """
    __tablename__ = 'tipo_texto'
    
    id_tipo_texto = Column(Integer, primary_key=True, index=True)
    nombre_tipo_texto = Column(String(50), nullable=False, unique=True)
    
    # Relación con los textos asociados
    textos = relationship("Texto", back_populates="tipo_texto")
