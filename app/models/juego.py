from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from app.core.database import Base

class Juego(Base):
    __tablename__ = "juego"

    id_juego = Column(Integer, primary_key=True, index=True)
    id_tipo_juego = Column(Integer, ForeignKey("tipo_juego.id_tipo_juego"))
    id_escenario = Column(Integer, ForeignKey("escenario.id_escenario"))
    id_nivel = Column(Integer, ForeignKey("nivel.id_nivel"))
    id_recompensa = Column(Integer, ForeignKey("recompensa.id_recompensa"))
    fecha_creacion = Column(DateTime)
    activo = Column(Boolean, default=True)
    nombre_juego = Column(ARRAY(String(100)), nullable=False)
    id_dificultad = Column(Integer, ForeignKey("dificultad.id_dificultad"))