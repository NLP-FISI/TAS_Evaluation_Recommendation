from fastapi import APIRouter, HTTPException
from app.services.evaluation_performance_service import calcular_desempenio
from app.schemas.evaluation_performance import ResultadoEvaluacion
from app.core.database import SessionLocal

router = APIRouter(prefix="/performance", tags=["Evaluación de desempeño"])

@router.post(
    "/evaluate/{id_usuario}",
    response_model=ResultadoEvaluacion,
    summary="Calcular el desempeño general del usuario",
    description="Procesa los datos del usuario y devuelve el cálculo final de su desempeño."
)
def evaluate_student(id_usuario: str):
    db = SessionLocal()
    try:
        result = calcular_desempenio(db, id_usuario)
        if not result:
            raise HTTPException(status_code=404, detail="No se pudo calcular el resultado")
        return result
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
    finally:
        db.close()