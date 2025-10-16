"""
Esquemas Pydantic para el módulo de profiling de usuarios.
"""
from pydantic import BaseModel, Field
from typing import List


class AvatarConfig(BaseModel):
    """Configuración del avatar del usuario."""
    body_type: str = Field(..., description="Tipo de cuerpo del avatar")
    face_type: str = Field(..., description="Tipo de cara del avatar")
    color: str = Field(..., description="Color principal del avatar")


class ProfilingRequest(BaseModel):
    """Modelo para la solicitud de perfilamiento."""
    student_id: str = Field(..., description="ID único del estudiante")
    grade_level: int = Field(..., ge=2, le=6, description="Grado escolar (2do a 6to)")
    preferences: List[str] = Field(..., min_items=1, description="Lista de temáticas de interés")
    avatar: AvatarConfig


class ProfilingResponse(BaseModel):
    """Modelo para la respuesta de perfilamiento."""
    student_id: str
    profile_created: bool
    message: str
