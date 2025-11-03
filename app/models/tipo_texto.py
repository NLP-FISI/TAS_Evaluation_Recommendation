from sqlalchemy import Column, Integer, String
from app.core.database import Base
from sqlalchemy.orm import relationship


class TipoTexto(Base):
    __tablename__ = "tipo_texto"  

    id_tipo_texto = Column(Integer, primary_key=True, index=True)
    nombre_tipo_texto = Column(String(50), nullable=False)

    # Relación con Texto
    textos = relationship("Texto", back_populates="tipo_texto")
