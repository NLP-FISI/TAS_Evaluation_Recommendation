# app/services/text_recommendation_service.py
import os
import httpx
from dotenv import load_dotenv
from app.models.usuario import Usuario
from app.services.recommendation_tipo_texto_service import recomendar_tipo_texto
# asegúrate de tener este
from app.services.recommendation_tematica_service import recomendar_tematica
from app.models.tipo_texto import TipoTexto
from app.models.tematica import Tematica

# env_file = ".env.dev" if os.getenv("ENV") == "development" else ".env"
# load_dotenv(dotenv_path=env_file)

# API_GENERATION = os.getenv(
#     "API_GENERATION")

API_GENERATION = "https://tas-content-generation.onrender.com"
class TextRecommendationService:

    @staticmethod
    async def get_recommendations(id_usuario: int, db):
        """
        Integra los recomendadores y obtiene los textos generados
        desde la API externa /contenido/obtener
        """

        # 1️⃣ Obtener datos del usuario
        usuario = db.query(Usuario).filter(
            Usuario.id_usuario == id_usuario).first()
        if not usuario:
            return {"mensaje": "Usuario no encontrado."}

        # 2️⃣ Obtener recomendaciones de tipo de texto y temática
        tipo_texto_rec = recomendar_tipo_texto(usuario, db)
        tematica_rec = recomendar_tematica(usuario.id_usuario, db)


        id_tipo_texto = tipo_texto_rec["id_tipo_texto"]
        id_tematica = tematica_rec.id_tematica
        id_dificultad = 1  # default

        # 3️⃣ Construir payload para la API externa
        payload = {
            "id_usuario": id_usuario,
            "id_tipo_texto": id_tipo_texto,
            "id_tematica": id_tematica,
            "id_dificultad": id_dificultad
        }

        # 4️⃣ Hacer request al microservicio de generación
        url_externa = f"{API_GENERATION}/contenido/obtener"

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url_externa, params=payload)

            if response.status_code != 200:
                raise Exception(f"Error al obtener textos: {response.text}")

            data_json = response.json()

            # 5️⃣ Retornar exactamente la misma respuesta de la API de generación
            return data_json

        except httpx.RequestError as e:
            return {"error": f"Error de conexión con el microservicio: {str(e)}"}
        except Exception as e:
            return {"error": f"Error inesperado: {str(e)}"}
