# app/models/usuario.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from app.core.database import Base

class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_grado = Column(Integer, ForeignKey("grado.id_grado"), nullable=True)
    nombre_usuario = Column(String(50), nullable=False)
    apellido_usuario = Column(String(50), nullable=False)
    genero = Column(String(1), nullable=True)
    edad = Column(Integer, nullable=True)
    email = Column(String(50), unique=True, index=True, nullable=False)
    contrasena = Column(String(100), nullable=False)
    fecha_registro = Column(DateTime, nullable=True)
    activo = Column(Boolean, default=True, nullable=True)
    monedas = Column(Integer, default=0, nullable=True)
    puntos = Column(Integer, default=0, nullable=True)
    configuracion_avatar = Column(JSON, nullable=True)
    student_id = Column(String(100), unique=True, index=True, nullable=True)
    dificultad_acumulada = Column(Float, nullable=True)

    # Relaciones
    grado = relationship("Grado", back_populates="usuarios")
    desempenio = relationship("Desempenio", back_populates="usuario", uselist=False)
    resultado_texto = relationship("ResultadoTexto", back_populates="usuario")
    resultado_juego = relationship("ResultadoJuego", back_populates="usuario")

    # Relaciones con Tematica y la tabla de asociación
    preferencias = relationship(
        "Tematica",
        secondary="usuario_preferencia",
        back_populates="usuarios"
    )

    usuario_preferencias = relationship(
        "UsuarioPreferencia",
        back_populates="usuario",
        overlaps="preferencias"
    )
