from sqlalchemy import Column, Integer, String
from app.core.database import Base

class TipoJuego(Base):
    __tablename__ = "tipo_juego"

    id_tipo_juego = Column(Integer, primary_key=True, index=True)
    nombre_tipo_juego = Column(String(50))
    descripcion = Column(String(200))