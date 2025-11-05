from fastapi import APIRouter, HTTPException
from typing import List
from app.services.evaluation_performance_service import (
    obtener_datos_bd,
    calcular_desempenio
)
from app.schemas.evaluation_performance import RegistroEvaluacionSalida, ResultadoEvaluacion
from app.core.database import SessionLocal

router = APIRouter(prefix="/performance", tags=["Evaluación de desempeño"])

@router.get("/data/{id_usuario}", response_model=List[RegistroEvaluacionSalida])
def get_performance_data(id_usuario: str):
    db = SessionLocal()
    try:
        data = obtener_datos_bd(db, id_usuario)
        if not data:
            raise HTTPException(status_code=404, detail="No se encontraron registros")
        return data
    finally:
        db.close()

@router.post("/evaluate/{id_usuario}", response_model=ResultadoEvaluacion)
def evaluate_student(id_usuario: str):
    db = SessionLocal()
    try:
        result = calcular_desempenio(id_usuario)
        if not result:
            raise HTTPException(status_code=404, detail="No se pudo calcular el resultado")
        return result
    finally:
        db.close()