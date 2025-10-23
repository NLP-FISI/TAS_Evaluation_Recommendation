from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

# Tabla de unión para la relación muchos a muchos entre Usuario y Tematica
usuario_preferencia_table = Table('usuario_preferencia', Base.metadata,
    Column('usuario_id', Integer, ForeignKey('usuario.id_usuario'), primary_key=True),
    Column('tematica_id', Integer, ForeignKey('tematica.id_tematica'), primary_key=True)
)

class Tematica(Base):
    """
    Modelo SQLAlchemy que representa la tabla 'tematica'.
    """
    __tablename__ = 'tematica'

    id_tematica = Column(Integer, primary_key=True, index=True)
    nombre_tematica = Column(String(50), unique=True, nullable=False)

    # Relación inversa para saber qué usuarios tienen esta temática
    usuarios = relationship(
        "Usuario",
        secondary=usuario_preferencia_table,
        back_populates="preferencias"
    )