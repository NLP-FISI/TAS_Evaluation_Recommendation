from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.schemas.recommendation_schemas import PreguntaOut
from app.services.recommendation_questions_service import filtrar_preguntas_por_dificultad
from app.core.database import get_db

router = APIRouter(
    prefix="/recommendation-questions",
    tags=["Recomendación de Preguntas"],
    responses={404: {"description": "Not found"}}
)

@router.get(
        "/", 
        response_model=list[PreguntaOut],
        summary="Filtrar preguntas por dificultad recomendada",
        description="""
            Filtra y retorna preguntas según el nivel de dificultad recomendado.

            - Dificultad: Nivel de dificultad recomendado (1-5).
            - Devuelve una lista de preguntas alineadas al nivel solicitado o al más cercano disponible.
                """,
        )
def get_preguntas_por_dificultad(
    dificultad: int = Query(..., ge=1, le=5),
    db: Session = Depends(get_db)
):
    preguntas = filtrar_preguntas_por_dificultad(db, dificultad)
    return preguntas