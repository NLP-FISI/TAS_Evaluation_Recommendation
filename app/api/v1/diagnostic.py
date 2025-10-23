"""
Router para los endpoints relacionados con el diagnóstico inicial.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.diagnostic_schemas import DiagnosticStage1Request, DiagnosticStage1Response
from app.services.diagnostic_service import DiagnosticService
from app.core.database import get_db # Importamos la dependencia get_db

# Crear el router para las rutas de diagnóstico
router = APIRouter(
    prefix="/diagnostic",
    tags=["Diagnostic"]
)

@router.post("/stage1", response_model=DiagnosticStage1Response)
async def submit_diagnostic_stage1(
    data: DiagnosticStage1Request,
    db: Session = Depends(get_db) # Inyectamos la sesión de BD
):
    """
    Endpoint para recibir y procesar las respuestas de la Etapa 1 del diagnóstico.
    Corresponde a la funcionalidad F-02.A.
    """
    try:
        return DiagnosticService.process_stage1(db=db, data=data)
    except HTTPException as http_exc:
        # Re-lanzar excepciones HTTP que ya vienen del servicio
        raise http_exc
    except Exception as e:
        # Capturar cualquier otro error inesperado
        print(f"Error inesperado en endpoint /diagnostic/stage1: {e}") # Log del error
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error interno al procesar la evaluación."
        )

