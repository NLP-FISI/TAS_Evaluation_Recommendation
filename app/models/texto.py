from sqlalchemy import Column, ForeignKey, Integer,String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

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
    resultado_texto = relationship("ResultadoTexto", back_populates="texto")
    