from fastapi import APIRouter, HTTPException, Depends
from app.schemas.recommendation_schemas import LastTextRequest
from app.services.recommendation_difficulty_service import actualizar_dificultad, obtener_promedio_dificultad_por_usuario_y_juego,obtener_resultado_general_juego
from app.schemas.recommendation_schemas import TextComplexityRequest, TextComplexityResponse, UpdateDifficultyRequest
from app.services.recommendation_difficulty_service import TextComplexityEvaluator
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.models.usuario import Usuario


router = APIRouter(prefix="/recommendation/difficulty",
                   tags=["Recommendation - Difficulty"])


#get para actualizar dificultad_acumulada
@router.post("/update")
def update_difficulty(request: UpdateDifficultyRequest, db: Session = Depends(get_db)):
    """
    Actualiza la dificultad acumulada de un usuario basado en su ID, el juego y el resultado obtenido.
    Usa como parámetro beta el promedio de dificultad de los textos asociados al usuario y al juego.
    """
    try:
        id_usuario = request.id_usuario
        id_juego = request.id_juego
        cal_resultado = obtener_resultado_general_juego(db,id_usuario,id_juego)
        resultado = cal_resultado["resultado_juego"]

        # Verificar usuario
        usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

         # Obtener el promedio de dificultad (llamando la función de /ultimo_texto)
        promedio_data = obtener_promedio_dificultad_por_usuario_y_juego(db, id_usuario, id_juego)

        if "promedio_dificultad" not in promedio_data:
            raise HTTPException(status_code=404, detail="No se encontró dificultad promedio para este usuario y juego")

        promedio_dificultad = float(promedio_data["promedio_dificultad"])

        # Calcular nueva dificultad
        theta_actual = usuario.dificultad_acumulada or 1

        theta, racha, beta_next, p = actualizar_dificultad(
            theta=theta_actual,
            racha=2,
            beta=promedio_dificultad,
            resultado=resultado
        )

        # Guardar cambios
        usuario.dificultad_acumulada = round(theta, 3)
        db.commit()

        # Respuesta
        return {
            "id_usuario": id_usuario,
            "id_juego": id_juego,
            "dificultad_acumulada_anterior": theta_actual,
            "dificultad_acumulada_actualizada": usuario.dificultad_acumulada,
            "promedio_dificultad_juego": promedio_dificultad,
            "recomendacion_de_dificultad": beta_next,  # VALOR DE DIFICULTAD RECOMENDADA PARA EL SIGUIENTE JUEGO(1-5)
            "correctas":cal_resultado["correctas"],
            "incorrectas":cal_resultado["incorrectas"],
            "resultado":cal_resultado["resultado_juego"]
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
