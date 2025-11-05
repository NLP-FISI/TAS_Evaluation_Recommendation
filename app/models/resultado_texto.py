# app/models/resultado_texto.py
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class ResultadoTexto(Base):
    __tablename__ = "resultado_texto"
    id_resultado_texto = Column(Integer, primary_key=True, index=True)
    id_texto = Column(Integer, ForeignKey("texto.id_texto"))
    id_juego = Column(Integer, ForeignKey("juego.id_juego"))
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"))
    tiempo = Column(DateTime)

    texto = relationship("Texto", back_populates="resultado_texto")
    juego = relationship("Juego", back_populates="resultado_texto")
    usuario = relationship("Usuario", back_populates="resultado_texto")
    