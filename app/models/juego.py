from sqlalchemy import Column, ForeignKey,Boolean, Integer,String, Text,DATETIME
from sqlalchemy.orm import relationship
from app.core.database import Base

class Juego(Base):
    __tablename__ = 'juego'
    id_juego = Column(Integer, primary_key=True, index=True)
    id_tipo_juego = Column(Integer)
    id_escenario = Column(Integer)
    id_nivel = Column(Integer)
    id_recompensa = Column(Integer)
    fecha_creation = Column(DATETIME)
    activo = Column(Boolean)
    nombre_juego = Column(String(100))
    id_dificultad = Column(Integer)

    resultado_texto = relationship("ResultadoTexto", back_populates="juego")
    resultado_juego = relationship("ResultadoJuego", back_populates="juego")
    