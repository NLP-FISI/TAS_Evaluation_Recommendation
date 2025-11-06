"""
Modelos SQLAlchemy para la aplicación.

Este archivo importa todos los modelos definidos en el directorio
y los expone para facilitar su uso en otras partes de la aplicación.
También asegura que todos los modelos usen la misma Base declarativa.
"""

# --- Base compartida ---
from app.core.database import Base

# --- Usuario y perfil ---
from .usuario import Usuario
from .grado import Grado
from .tematica import Tematica
from .desempenio import Desempenio

# --- Catálogos ---
from .tipo_texto import TipoTexto
from .tipo_pregunta import TipoPregunta
from .dificultad import Dificultad

# --- Contenido educativo ---
from .texto import Texto
from .pregunta import Pregunta
from .alternativa import Alternativa

# --- Diagnóstico ---
from .resultado_diagnostico import ResultadoDiagnostico

# --- Asociación Usuario–Temática ---
# (Solo si estás usando el modelo ORM completo)
from .usuario_preferencia import UsuarioPreferencia

# --- Otros modelos opcionales ---
# Si existen en tu estructura, se pueden importar sin romper compatibilidad
try:
    from .resultado_texto import ResultadoTexto
except ImportError:
    ResultadoTexto = None

try:
    from .juego import Juego
    from .resultado_juego import ResultadoJuego
except ImportError:
    Juego = None
    ResultadoJuego = None

# --- Recomendación / IA ---
from .recommendation import ExperienceLevel


# --- Exportación controlada ---
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
    # Asociación Usuario–Temática
    "UsuarioPreferencia",
    # Otros
    "ResultadoTexto",
    "Juego",
    "ResultadoJuego",
    "ExperienceLevel",
]
