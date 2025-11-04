# File: app/schemas/challenges_schemas.py
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from enum import Enum

# --- Modelos de Dominio para la Lógica de Retos ---

class RetoResultadoEnum(str, Enum):
    victoria_retador = "victoria_retador"
    victoria_contrincante = "victoria_contrincante"
    empate = "empate"

class DesempenoJugador(BaseModel):
    id_usuario: int = Field(..., description="ID único del jugador.")
    respuestas_correctas: int = Field(..., ge=0, description="Número de respuestas correctas.")
    tiempo_total_seg: float = Field(..., ge=0, description="Tiempo total en segundos que tardó en responder.")
    # Los campos de racha se eliminan de aquí porque ahora se calculan en el servidor.

class RetoParaEvaluar(BaseModel):
    retador: DesempenoJugador
    contrincante: DesempenoJugador
    
class ResultadoEvaluacion(BaseModel):
    id_ganador: Optional[int] = Field(description="ID del jugador ganador. Nulo si es empate.")
    id_retador: int
    rating_anterior_retador: int
    rating_nuevo_retador: int
    variacion_retador: int
    id_contrincante: int
    rating_anterior_contrincante: int
    rating_nuevo_contrincante: int
    variacion_contrincante: int
    mensaje: str
    mensaje_personalizado: Optional[str] = Field(None, description="Mensaje dinámico basado en el rendimiento.")

class UsuarioData(BaseModel):
    """
    Esquema para transportar los datos del usuario desde la BD al servicio.
    Usa la configuración moderna de Pydantic V2.
    """
    model_config = ConfigDict(from_attributes=True) # <-- ESTA ES LA LÍNEA CLAVE CORREGIDA

    id_usuario: int
    nombre_usuario: str
    puntos: int