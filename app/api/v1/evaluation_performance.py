from fastapi import APIRouter, HTTPException
from typing import List
from app.services.evaluation_performance_service import (
    get_raw_data_from_db,
    calculate_performance
)
from app.schemas.evaluation_performance import RegistroEvaluacionSalida, ResultadoEvaluacion

router = APIRouter(prefix="/performance", tags=["Evaluación de desempeño"])

@router.get("/data/{id_usuario}", response_model=List[RegistroEvaluacionSalida])
def get_performance_data(id_usuario: str):
    data = get_raw_data_from_db(id_usuario)
    if not data:
        raise HTTPException(status_code=404, detail="No se encontraron registros")
    return data

@router.post("/evaluate/{id_usuario}", response_model=ResultadoEvaluacion)
def evaluate_student(id_usuario: str):
    result = calculate_performance(id_usuario)
    return result
