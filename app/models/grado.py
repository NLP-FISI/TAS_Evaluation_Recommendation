from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class Grado(Base):
    __tablename__ = "grado"

    id_grado = Column(Integer, primary_key=True, index=True)
    nombre_grado = Column(String(50))
    cantidad_usuarios = Column(Integer)
    ciclo_grado = Column(Integer)

    usuarios = relationship("Usuario", back_populates="grado")
