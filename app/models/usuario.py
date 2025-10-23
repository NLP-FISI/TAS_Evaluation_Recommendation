# app/models/usuario.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True, index=True)
    id_grado = Column(Integer, ForeignKey("grado.id_grado"))
    nombre_usuario = Column(String(50))
    apellido_usuario = Column(String(50))
    genero = Column(String(1))
    edad = Column(Integer)
    email = Column(String(50))
    # ·contraseña = Column(String(50))
    fecha_registro = Column(DateTime)
    activo = Column(Boolean, default=True)
    monedas = Column(Integer, default=0)
    puntos = Column(Integer, default=0)
    configuracion_avatar = Column(JSON)
    id_tematica = Column(Integer)
    student_id = Column(String(50))

    grado = relationship("Grado", back_populates="usuarios")
    desempenio = relationship("Desempenio", back_populates="usuario")
