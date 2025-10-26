from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Desempenio(Base):
    __tablename__ = "desempenio"

    id_desempenio = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey(
        "usuario.id_usuario"), unique=True, nullable=False)

    puntaje = Column(Numeric(5, 2), nullable=False)
    nivel = Column(String(20), nullable=False)
    exactitud = Column(Numeric(4, 3), nullable=False)
    promedio_tiempo_por_pregunta = Column(Numeric(8, 2), nullable=False)
    promedio_tiempo_por_lectura = Column(Numeric(8, 2), nullable=False)
    textos_considerados = Column(Integer, nullable=False)

    # Relación inversa
    usuario = relationship("Usuario", back_populates="desempenio")
