from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Nivel(Base):
    __tablename__ = "nivel"

    id_nivel = Column(Integer, primary_key=True, index=True)
    nombre_nivel = Column(String(50))
    descripcion_nivel = Column(String(200))