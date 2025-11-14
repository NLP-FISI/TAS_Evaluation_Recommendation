# app/models/desempenio.py
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Desempenio(Base):
    """
    Representa el desempeño general y el nivel de un usuario.
    """
    __tablename__ = "desempenio"

    id_desempenio = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False, index=True)

    # Columna para almacenar el puntaje numérico
    puntaje = Column(Numeric(5, 2), nullable=True)

    # Columna para la etiqueta descriptiva del nivel (ej. "4to Grado")
    nivel = Column(String(20), nullable=True)

    # Exactitud del usuario (numeric(4,3) en la BD)
    exactitud = Column(Numeric(4, 3), nullable=True)

    # Promedios de tiempo
    promedio_tiempo_por_pregunta = Column(Numeric(8, 2), nullable=True)
    promedio_tiempo_por_lectura = Column(Numeric(8, 2), nullable=True)

    # Textos considerados
    textos_considerados = Column(Integer, nullable=True)

    # ID del grado de competencia (2, 3, 4, 5, 6)
    nivel_grado_id = Column(Integer, ForeignKey("grado.id_grado"), nullable=True)

    # Relaciones
    usuario = relationship("Usuario", back_populates="desempenio")
    grado_competencia = relationship("Grado")
