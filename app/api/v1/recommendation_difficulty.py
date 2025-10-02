from fastapi import APIRouter

router = APIRouter(
    prefix="/recommendation_difficulty",
    tags=["dificultad input"]
)


#get principal para obtener dificultad_acumulada
@router.get("/{id_user}")
def read_difficulty(id_user: str):
    return {f"dificultad obtenida de {id_user}"}

#get para actualizar dificultad_acumulada

#get para obtener dicicultad_acumulada anterior

#get para obtener racha
