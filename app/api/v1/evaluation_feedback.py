# app/api/v1/evaluation_feedback.py
from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List, Dict
from app.core.e07.evaluate_once import FeedbackEmbeddingEvaluator

router = APIRouter(prefix="/feedback", tags=["feedback"])

_evaluator = FeedbackEmbeddingEvaluator()

class EvalReq(BaseModel):
    mensaje_texto: str = Field(..., min_length=3)
    tipo_error: str
    grado: int
    pistas: List[str] = []

class EvalRes(BaseModel):
    similaridad_error: float
    ok: bool
    razones: Dict

@router.post("/evaluate", response_model=EvalRes)
def evaluate(req: EvalReq):
    return _evaluator.evaluate(
        mensaje_texto=req.mensaje_texto,
        tipo_error=req.tipo_error,
        grado=req.grado,
        pistas=req.pistas
    )
