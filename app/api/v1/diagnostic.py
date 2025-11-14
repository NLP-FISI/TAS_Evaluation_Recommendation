# File: app/api/v1/diagnostic.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


# Importar dependencias y servicios
from app.core.database import get_db
from app.services.diagnostic_service import DiagnosticService
from app.schemas.diagnostic_schemas import (
    DiagnosticStage1Request, DiagnosticStage1Response,
    DiagnosticStage2Request, DiagnosticStage2Response,
    LevelAssignmentRequest, LevelAssignmentResponse  # Importar nuevos esquemas
)

# Crear el router para las rutas de diagnóstico
router = APIRouter(
    prefix="/diagnostic",
    tags=["Diagnostic"]
)

@router.post("/stage1", response_model=DiagnosticStage1Response)
async def process_diagnostic_stage1(
    data: DiagnosticStage1Request,
    db: Session = Depends(get_db)
):
    """
    Endpoint para procesar las respuestas de la Etapa 1 del diagnóstico (F-02.A).
    Recibe las 2 respuestas, las evalúa, guarda los resultados y
    devuelve la decisión ('CONTINUAR' o 'FINALIZAR').
    """
    try:
        # Pasamos la sesión de BD al servicio
        return DiagnosticService.process_stage1(data, db)
    except HTTPException as http_exc:
        raise http_exc # Re-lanzar excepciones conocidas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en Etapa 1: {str(e)}")


@router.post("/stage2", response_model=DiagnosticStage2Response)
async def process_diagnostic_stage2(
    data: DiagnosticStage2Request,
    db: Session = Depends(get_db)
):
    """
    Endpoint para procesar las respuestas de la Etapa 2 del diagnóstico (F-02.B).
    Recibe las 3 respuestas, las evalúa y guarda los resultados.
    """
    try:
        # Pasamos la sesión de BD al servicio
        return DiagnosticService.process_stage2(data, db)
    except HTTPException as http_exc:
        raise http_exc # Re-lanzar excepciones conocidas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en Etapa 2: {str(e)}")

# --- ¡NUEVO ENDPOINT PARA F-03! ---
@router.post("/assign-level", response_model=LevelAssignmentResponse)
async def assign_initial_level(
    data: LevelAssignmentRequest,
    db: Session = Depends(get_db)
):
    """
    Endpoint para calcular y asignar el nivel de competencia inicial (F-03).
    Lee los resultados guardados de Etapa 1 y 2, y guarda el nivel final
    en el registro de Desempeño del usuario.
    """
    try:
        # Pasamos la sesión de BD al servicio
        return DiagnosticService.assign_initial_level(data, db)
    except HTTPException as http_exc:
        raise http_exc # Re-lanzar excepciones conocidas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno al asignar nivel: {str(e)}")
