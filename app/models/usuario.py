from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON, Float, Table
from sqlalchemy.orm import relationship
from app.core.database import Base

# Tabla de unión para la relación muchos a muchos entre Usuario y Tematica
usuario_preferencia_table = Table('usuario_preferencia', Base.metadata,
    Column('usuario_id', Integer, ForeignKey('usuario.id_usuario'), primary_key=True),
    Column('tematica_id', Integer, ForeignKey('tematica.id_tematica'), primary_key=True)
)

class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(100), unique=True, index=True, nullable=False)
    id_grado = Column(Integer, ForeignKey("grado.id_grado"))
    id_dificultad = Column (Integer)
    nombre_usuario = Column(String(50), nullable=False)
    apellido_usuario = Column(String(50), nullable=False)
    contrasena = Column(String(255), nullable=False)  # Campo requerido
    genero = Column(String(1))
    edad = Column(Integer)
    email = Column(String(50), unique=True, index=True)
    fecha_registro = Column(DateTime)
    activo = Column(Boolean, default=True)
    monedas = Column(Integer, default=0)
    puntos = Column(Integer, default=0)
    configuracion_avatar = Column(JSON)
    id_tematica = Column(Integer)
    dificultad_acumulada = Column(Float)

    # Relaciones
    grado = relationship("Grado", back_populates="usuarios")
    
    # Relación muchos a muchos con la tabla Tematica a través de la tabla de unión
    preferencias = relationship(
        "Tematica",
        secondary=usuario_preferencia_table,
        back_populates="usuarios"
    )
