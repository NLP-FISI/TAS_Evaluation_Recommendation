"""Modelo para tipos de texto (narrativo, expositivo, argumentativo, etc.)"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class TipoTexto(Base):
    __tablename__ = 'tipo_texto'
    
    id_tipo_texto = Column(Integer, primary_key=True, index=True)
    nombre_tipo_texto = Column(String(50), nullable=False, unique=True)
    
    textos = relationship("Texto", back_populates="tipo_texto")
