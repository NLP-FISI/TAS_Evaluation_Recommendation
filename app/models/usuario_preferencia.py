# app/models/usuario_preferencia.py
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class UsuarioPreferencia(Base):
    """
    Represents the association between a Usuario and a Tematica.
    Mapped to the "usuario_preferencia" table, this class implements a simple
    many-to-many association (association table / association object) between the
    Usuario and Tematica models.
    Attributes
    ----------
    usuario_id : int
        Foreign key referencing Usuario.id_usuario. Part of the composite primary key.
    tematica_id : int
        Foreign key referencing Tematica.id_tematica. Part of the composite primary key.
    usuario : Usuario
        Optional SQLAlchemy relationship to the associated Usuario object.
        Uses back_populates="usuario_preferencias" to mirror the relationship.
    tematica : Tematica
        Optional SQLAlchemy relationship to the associated Tematica object.
        Uses back_populates="usuario_preferencias" to mirror the relationship.
    Notes
    -----
    - The combination of (usuario_id, tematica_id) forms a composite primary key,
      enforcing that each user–thematic preference pair is unique.
    - Because this is modeled as an association object, additional columns such as
      timestamps or preference weights can be added later if richer semantics are
      required.
    - Designed to be used with a declarative SQLAlchemy Base.
    """
    
    __tablename__ = "usuario_preferencia"

    usuario_id = Column(Integer, ForeignKey(
        "usuario.id_usuario"), primary_key=True)
    tematica_id = Column(Integer, ForeignKey(
        "tematica.id_tematica"), primary_key=True)

    # Opcional: relaciones hacia Usuario y Tematica
    usuario = relationship("Usuario", back_populates="usuario_preferencias")
    tematica = relationship("Tematica", back_populates="usuario_preferencias")
