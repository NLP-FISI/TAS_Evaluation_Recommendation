from sqlalchemy import Column, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


class ResultadoJuego(Base):
    __tablename__ = "resultado_juego"
    id_resultado_juego = Column(Integer, primary_key=True, index=True)
    id_juego = Column(Integer, ForeignKey("juego.id_juego"))
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"))
    #id_dificultad = Column(Integer)
    tiempo_texto_seg = Column(DateTime)
    tiempo_pregunta_seg = Column(DateTime)
    completado = Column(Boolean)
    correctas = Column(Integer)
    incorrectas = Column(Integer)
    fecha_inicio = Column(DateTime)
    fecha_final = Column(DateTime)

    juego = relationship("Juego", back_populates="resultado_juego")
    usuario = relationship("Usuario", back_populates="resultado_juego")