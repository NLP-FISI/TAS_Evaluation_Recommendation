from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Desempenio(Base):
    __tablename__ = "desempenio"

    id_desempenio = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"))
    puntaje = Column(Integer)
    nivel = Column(String(50))
    exactitud = Column(Integer)
    promedio_tiempo_por_pregunta = Column(Integer)
    promedio_tiempo_por_lectura = Column(Integer)
    textos_considerados = Column(Integer)

    usuario = relationship("Usuario", back_populates="desempenio")
