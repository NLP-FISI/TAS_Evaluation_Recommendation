"""
Modelos SQLAlchemy para la aplicación.

Este archivo importa todos los modelos definidos en el directorio
y los expone para facilitar su uso en otras partes de la aplicación.
También asegura que todos los modelos usen la misma Base declarativa.
"""

# Importar la Base compartida
from app.core.database import Base

# Importar modelos de los diferentes archivos
from .user_profile import Usuario, Grado, Tematica, usuario_preferencia_table
from .diagnostic import Texto, Pregunta, Alternativa, ResultadoDiagnostico, TipoPregunta, Dificultad, TipoTexto
from .recommendation import ExperienceLevel
# Asumiendo que Desempenio está en su propio archivo
try:
    from .desempenio import Desempenio
except ImportError:
    # Manejar caso si desempenio.py no existe aún o tiene otro nombre
    Desempenio = None

# Lista __all__ para controlar 'from app.models import *'
# Incluye todos los nombres de las CLASES de modelos (y Base)
__all__ = [
    "Base",
    "Usuario",
    "Grado",
    "Tematica",
    "Texto",
    "Pregunta",
    "Alternativa",
    "ResultadoDiagnostico",
    "TipoPregunta",
    "Dificultad",
    "TipoTexto",
    "ExperienceLevel",
    *(["Desempenio"] if Desempenio else [])
    # Nota: No solemos incluir las tablas de unión (como usuario_preferencia_table) en __all__
]

# Opcional: Verificar si Desempenio se pudo importar
if Desempenio is None:
    print("Advertencia: No se pudo importar el modelo Desempenio desde app.models.desempenio")
