from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from app.core.database import Base


class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True, index=True)
    id_grado = Column(Integer, ForeignKey("grado.id_grado"))
    id_dificultad = Column (Integer, ForeignKey("dificultad.id_dificultad"))
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
    dificultad_acumulada = Column(Float)

    grado = relationship("Grado", back_populates="usuarios")
    desempenio = relationship("Desempenio", back_populates="usuario")
    dificultad = relationship("Dificultad", back_populates="usuarios")
