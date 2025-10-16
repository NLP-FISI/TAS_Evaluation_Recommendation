"""
Modelos SQLAlchemy para la aplicación.
"""
from .user_profile import Usuario, Tematica, Grado, UsuarioTematica, Base

__all__ = [
    "Usuario",
    "Tematica", 
    "Grado",
    "UsuarioTematica",
    "Base"
]