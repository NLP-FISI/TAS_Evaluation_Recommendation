# app/models/usuario_preferencia.py
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class UsuarioPreferencia(Base):
    """
    Modelo de asociación entre Usuario y Tematica.
    Representa la tabla 'usuario_preferencia' como una clase ORM,
    permitiendo relaciones bidireccionales y futura extensión con más atributos.
    """

    __tablename__ = "usuario_preferencia"

    usuario_id = Column(Integer, ForeignKey("usuario.id_usuario"), primary_key=True)
    tematica_id = Column(Integer, ForeignKey("tematica.id_tematica"), primary_key=True)

    # Relaciones hacia los modelos principales
    usuario = relationship("Usuario", back_populates="usuario_preferencias")
    tematica = relationship("Tematica", back_populates="usuario_preferencias")

    def __repr__(self):
        return f"<UsuarioPreferencia(usuario_id={self.usuario_id}, tematica_id={self.tematica_id})>"
