"""
Esquemas Pydantic para el módulo de profiling de usuarios.
"""
from pydantic import BaseModel, Field
from typing import List


class ProfilingRequest(BaseModel):
    """Modelo para la solicitud de perfilamiento."""
    student_id: str = Field(..., description="ID único del estudiante")
    grade_level: int = Field(..., ge=2, le=6, description="Grado escolar (2do a 6to)")
    preferences: List[int] = Field(..., min_items=1, description="Lista de IDs de temáticas de interés (de la tabla tematica)")


class ProfilingResponse(BaseModel):
    """Modelo para la respuesta de perfilamiento."""
    student_id: str
    profile_created: bool
    message: str
