from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base

class Reto(Base):
    __tablename__ = "reto"

    id_reto = Column(Integer, primary_key=True, index=True)
    id_juego = Column(Integer, ForeignKey("juego.id_juego"))
    id_usuario_retador = Column(Integer, ForeignKey("usuario.id_usuario"))
    id_usuario_contrincante = Column(Integer, ForeignKey("usuario.id_usuario"))
    estado = Column(String)
    ganador = Column(Integer, nullable=True)