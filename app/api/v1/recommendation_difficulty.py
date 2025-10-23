from fastapi import APIRouter, HTTPException, Depends
from app.schemas.recommendation_schemas import RecommendationDifficultyRequest
from app.services.recommendation_difficulty_service import actualizar_dificultad
from app.schemas.recommendation_schemas import TextComplexityRequest, TextComplexityResponse
from app.services.recommendation_difficulty_service import TextComplexityEvaluator
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.models.usuario import Usuario


router = APIRouter(prefix="/recommendation/difficulty",
                   tags=["Recommendation - Difficulty"])

#get principal para obtener dificultad_acumulada
@router.get("/difi/{id_user}")
def read_difficulty(id_user: str):
    return {f"dificultad obtenida de {id_user}"}

#get para actualizar dificultad_acumulada

@router.get("/update/{id}")
def update_difficulty(id: int, resultado: int, db: Session = Depends(get_db)):
    """
    Actualiza la dificultad acumulada de un usuario basado en su ID y el resultado obtenido.
    """
    try:
        usuario = db.query(Usuario).filter(Usuario.id_usuario == id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        theta_actual = usuario.dificultad_acumulada or 1  # si es None, usar 1

        theta, racha, beta_next, p = actualizar_dificultad(
            theta=theta_actual,
            racha=2,
            beta=3,
            resultado=resultado
        )

        usuario.dificultad_acumulada = round(theta, 3)
        db.commit()

        return {
            "id_user": id,
            "dificultad_acumulada_anterior": theta_actual,
            "dificultad_acumulada_actualizada": usuario.dificultad_acumulada,
            "recomendacion_de_dificultad": beta_next
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar la dificultad: {str(e)}")

#get para obtener dicicultad_acumulada anterior

@router.post("/evaluate", response_model=TextComplexityResponse)
async def evaluate_content_complexity(request: TextComplexityRequest):
    """
    RF4 - Validación Externa de la Complejidad del Contenido.
    Analiza un texto y devuelve su nivel de complejidad y puntuación cuantitativa.
    """
    try:
        evaluator = TextComplexityEvaluator()
        result = evaluator.evaluate_text(request.content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
