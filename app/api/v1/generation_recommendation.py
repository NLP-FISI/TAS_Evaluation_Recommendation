from fastapi import APIRouter, HTTPException
import httpx
from app.schemas.recommendation_schemas import RecommendationGenerationRequest,RecommendationGenerationResponse
import os
from dotenv import load_dotenv

env_file = ".env.dev" if os.getenv("ENV") == "development" else ".env"
load_dotenv(dotenv_path=env_file)


router = APIRouter(
    prefix="/recommendation-generation",
    tags=["Generation Recommendation"]
)

@router.post("/obtener-textos", response_model=RecommendationGenerationResponse)
async def obtener_textos(data: RecommendationGenerationRequest):
    """
    Recibe los 4 IDs, hace una llamada GET al endpoint externo
    /ejemplo/contenido/obtener y devuelve la respuesta en el formato BaseModel.
    """
    url_externa = f"{os.getenv("API_GENERATION")}/contenido/obtener"

    params = {
        "id_usuario": data.id_usuario,
        "id_tipo_texto": data.id_tipo_texto,
        "id_tematica": data.id_tematica,
        "id_dificultad": data.id_dificultad,
        "cantidad": 1
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url_externa, params=params)

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Error al obtener los textos: {response.text}"
            )

        data_json = response.json()
        return RecommendationGenerationResponse(**data_json)

    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")
