from sqlalchemy import Column, Integer
from app.core.database import Base

class Recompensa(Base):
    __tablename__ = "recompensa"

    id_recompensa = Column(Integer, primary_key=True, index=True)
    id_tipo_recompensa = Column(Integer)
    cantidad = Column(Integer)