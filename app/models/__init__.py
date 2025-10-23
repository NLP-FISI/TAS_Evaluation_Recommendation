"""
Modelos SQLAlchemy para la aplicación.
"""

from .usuario import Usuario
from .desempenio import Desempenio
from .grado import Grado  # si existe
# from .tematica import Tematica  # si existe

__all__ = [
    "Usuario",
    "Desempenio",
    "Grado",
    # "Tematica"
]
