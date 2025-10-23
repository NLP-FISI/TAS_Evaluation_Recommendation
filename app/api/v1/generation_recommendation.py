from fastapi import APIRouter, HTTPException, Depends
import httpx
from app.schemas.recommendation_schemas import RecommendationGenerationRequest,RecommendationGenerationResponse
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.usuario import Usuario

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
    /contenido/obtener y devuelve la respuesta en el formato BaseModel.
    """
    url_externa = f"{os.getenv('API_GENERATION')}/contenido/obtener"

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
    

@router.post("/obtener-textos-v2", response_model=RecommendationGenerationResponse)
async def obtener_textos(data: RecommendationGenerationRequest, db: Session = Depends(get_db)):
    """
    Obtiene la dificultad acumulada del usuario y la usa como id_dificultad redondeado.
    Luego hace una llamada GET al endpoint externo /contenido/obtener.
    """

    #Buscar al usuario en la base de datos
    usuario = db.query(Usuario).filter(Usuario.id_usuario == data.id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    #Obtener el valor actual de dificultad acumulada
    # dificultad_acumulada = usuario.dificultad_acumulada or 1
    try:
        dificultad_acumulada = usuario.dificultad_acumulada if usuario.dificultad_acumulada is not None else 1
    except AttributeError:
        dificultad_acumulada = 1
    id_dificultad = round(dificultad_acumulada)

    #Construir la URL externa y parámetros
    url_externa = f"{os.getenv('API_GENERATION')}/contenido/obtener"

    params = {
        "id_usuario": data.id_usuario,
        "id_tipo_texto": data.id_tipo_texto,# ENPOINT TIPO DE TEXTO?
        "id_tematica": data.id_tematica, #ENDPOINT TEMATICA?
        "id_dificultad": id_dificultad, #round(valor dificultad acumulada obtenido de la tabla usuarios 1-5)
        "cantidad": 1
    }

    #Llamada al endpoint externo
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url_externa, params=params)

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Error al obtener los textos: {response.text}"
            )

        #Respuesta
        data_json = response.json()
        return RecommendationGenerationResponse(**data_json)

    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")
