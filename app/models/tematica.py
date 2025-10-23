from sqlalchemy import Column, Integer, String
from app.core.database import Base


class Tematica(Base):
    __tablename__ = "tematica"

    id_tematica = Column(Integer, primary_key=True, index=True)
    nombre_tematica = Column(String(50), nullable=False)
