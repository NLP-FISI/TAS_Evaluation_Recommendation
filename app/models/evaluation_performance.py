from sqlalchemy import Column, String, Float, Integer, ForeignKey
from app.core.database import Base

class RegistroEvaluacion(Base):
    __tablename__ = "resultado_juego"

    id_resultado_juego = Column(String, primary_key=True, index=True)
    id_usuario = Column(String, ForeignKey("usuarios.id"), nullable=False)
    tiempo_texto_seg = Column(Float, nullable=False)
    tiempo_pregunta_seg = Column(Float, nullable=False)
    correctas = Column(Integer, nullable=False)
    incorrectas = Column(Integer, nullable=False)