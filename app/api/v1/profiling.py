"""
Router para endpoints de profiling de usuarios (versión simplificada sin DB).
"""
from fastapi import APIRouter

from app.schemas.profiling_schemas import ProfilingRequest, ProfilingResponse
from app.services.profiling_service import ProfilingService

# Crear el router para las rutas de profiling
router = APIRouter(
    prefix="/profiling",
    tags=["User Profiling"]
)

@router.post("/", response_model=ProfilingResponse)
async def create_user_profile(data: ProfilingRequest):
    """
    Endpoint para el perfilamiento inicial del usuario.
    Registra el grado escolar, intereses y configuración del avatar.
    Corresponde a la funcionalidad F-01.
    """
    return ProfilingService.create_profile(data)

