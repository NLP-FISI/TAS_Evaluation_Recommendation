"""
Router para endpoints de profiling de usuarios.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.profiling_schemas import ProfilingRequest, ProfilingResponse
from app.services.profiling_service import ProfilingService
from app.core.database import get_db

# Crear el router para las rutas de profiling
router = APIRouter(
    prefix="/profiling",
    tags=["User Profiling"]
)

@router.post("/", response_model=ProfilingResponse)
async def create_user_profile(
    data: ProfilingRequest, 
    db: Session = Depends(get_db)
):
    """
    Endpoint para el perfilamiento inicial del usuario.
    Registra el grado escolar, intereses y configuración del avatar en PostgreSQL.
    Corresponde a la funcionalidad F-01.
    """
    return ProfilingService.create_profile(data, db)

