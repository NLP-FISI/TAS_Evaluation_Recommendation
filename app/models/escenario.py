from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Escenario(Base):
    __tablename__ = "escenario"

    id_escenario = Column(Integer, primary_key=True, index=True)
    nombre_escenario = Column(String(50))
    niveles_requeridos = Column(Integer)