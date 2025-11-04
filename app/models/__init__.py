"""
Modelos SQLAlchemy para la aplicación.

Este archivo importa todos los modelos definidos en el directorio
y los expone para facilitar su uso en otras partes de la aplicación.
También asegura que todos los modelos usen la misma Base declarativa.
"""

# Importar la Base compartida
from app.core.database import Base

# Importar modelos de usuario y perfil
from .usuario import Usuario
from .grado import Grado
from .tematica import Tematica, usuario_preferencia_table
from .desempenio import Desempenio

# Importar catálogos
from .tipo_texto import TipoTexto
from .tipo_pregunta import TipoPregunta
from .dificultad import Dificultad

# Importar contenido educativo
from .texto import Texto
from .pregunta import Pregunta
from .alternativa import Alternativa

# Importar diagnóstico
from .resultado_diagnostico import ResultadoDiagnostico

# Importar otros modelos
from .recommendation import ExperienceLevel

# Lista __all__ para controlar 'from app.models import *'
__all__ = [
    "Base",
    # Usuario y perfil
    "Usuario",
    "Grado",
    "Tematica",
    "Desempenio",
    # Catálogos
    "TipoTexto",
    "TipoPregunta",
    "Dificultad",
    # Contenido educativo
    "Texto",
    "Pregunta",
    "Alternativa",
    # Diagnóstico
    "ResultadoDiagnostico",
    # Otros
    "ExperienceLevel",
]
