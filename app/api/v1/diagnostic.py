# File: app/api/v1/diagnostic.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


# Importar dependencias y servicios
from app.core.database import get_db
from app.services.diagnostic_service import DiagnosticService
from app.schemas.diagnostic_schemas import (
    DiagnosticStage1Request, DiagnosticStage1Response,
    DiagnosticStage2Request, DiagnosticStage2Response
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
        return DiagnosticService.process_stage1(data, db)
    except HTTPException as http_exc:
        # Re-lanzar excepciones HTTP tal cual
        raise http_exc
    except Exception as e:
        # Capturar otros errores inesperados
        print(f"Error inesperado en /diagnostic/stage1: {e}") # Log del error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocurrió un error interno al procesar la Etapa 1: {e}"
        )


@router.post("/stage2", response_model=DiagnosticStage2Response)
async def process_diagnostic_stage2(
    data: DiagnosticStage2Request,
    db: Session = Depends(get_db)
):
    """
    Endpoint para procesar las respuestas de la Etapa 2 del diagnóstico (F-02.B).
    Recibe las 3 respuestas, las evalúa y guarda los resultados.
    La asignación final de nivel (Intermedio/Avanzado) se hará en F-03.
    """
    try:
        return DiagnosticService.process_stage2(data, db)
    except HTTPException as http_exc:
        # Re-lanzar excepciones HTTP tal cual
        raise http_exc
    except Exception as e:
        # Capturar otros errores inesperados
        print(f"Error inesperado en /diagnostic/stage2: {e}") # Log del error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocurrió un error interno al procesar la Etapa 2: {e}"
        )

# --- Endpoint Opcional para Obtener Contenido ---
# @router.get("/stage1/content")
# async def get_stage1_content(db: Session = Depends(get_db)):
#     """
#     (Opcional) Endpoint para que el frontend obtenga el texto y las preguntas
#     de la Etapa 1. Debería buscar en la BD el texto y preguntas con IDs fijos.
#     """
#     # Lógica para buscar Texto con ID 1, Preguntas 1 y 2, y sus Alternativas
#     # ...
#     # Devolverlos en un formato JSON adecuado para el frontend
#     pass

# @router.get("/stage2/content")
# async def get_stage2_content(db: Session = Depends(get_db)):
#     """
#     (Opcional) Endpoint para que el frontend obtenga el texto y las preguntas
#     de la Etapa 2. Debería buscar en la BD el texto y preguntas con IDs fijos.
#     """
#     # Lógica para buscar Texto con ID 2, Preguntas 3, 4 y 5, y sus Alternativas
#     # ...
#     # Devolverlos en un formato JSON adecuado para el frontend
#     pass

