# app/models/respuesta_usuario.py
from sqlalchemy import Column, Integer, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class RespuestaUsuario(Base):
    __tablename__ = "respuesta_usuario"

    id_respuesta = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    id_actividad = Column(Integer, nullable=False)
    id_pregunta = Column(Integer, ForeignKey("pregunta.id_pregunta"), nullable=False)
    id_alternativa = Column(Integer, nullable=False)
    es_correcta = Column(Boolean)
    fecha_respuesta = Column(DateTime(timezone=True), server_default=func.now())
