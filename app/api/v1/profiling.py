"""
Router para endpoints de profiling de usuarios.
"""
from fastapi import APIRouter

# Inicializar el router primero
router = APIRouter(
    prefix="/profiling",
    tags=["User Profiling"]
)

# Importar dependencias después del router
from app.schemas.profiling_schemas import ProfilingRequest, ProfilingResponse
from app.services.profiling_service import ProfilingService


@router.post("/", response_model=ProfilingResponse)
async def create_user_profile(data: ProfilingRequest):
    """
    Endpoint para el perfilamiento inicial del usuario.
    Registra el grado escolar, intereses y configuración del avatar.
    Corresponde a la funcionalidad F-01.
    """
    return ProfilingService.create_profile(data)
