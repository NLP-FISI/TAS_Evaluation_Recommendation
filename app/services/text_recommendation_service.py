import httpx
from app.models.usuario import Usuario

from app.services.recommendation_tipo_texto_service import recomendar_tipo_texto

API_GENERATION = "https://tas-content-generation.onrender.com"


class TextRecommendationService:
    """
    A service class for handling text recommendations based on user preferences and interactions.
    This class provides functionality to generate personalized text recommendations by integrating
    different recommendation systems and communicating with an external content generation API.
    Methods:
        get_recommendations(id_usuario: int, db) -> dict:
            Retrieves personalized text recommendations for a specific user by:
            - Fetching user data from the database
            - Determining recommended text types based on user profile
            - Obtaining topic preferences
            - Making requests to external content generation API
    Returns:
        dict: Response from the content generation API containing recommended texts
              or an error message if the process fails
    Raises:
        httpx.RequestError: If there's an error connecting to the external microservice
        Exception: For unexpected errors during the recommendation process
    """

    @staticmethod
    async def get_recommendations(id_usuario: int, db):
        """
        Integra los recomendadores y obtiene los textos generados
        desde la API externa /contenido/obtener
        """

        # Obtener datos del usuario
        usuario = db.query(Usuario).filter(
            Usuario.id_usuario == id_usuario).first()
        if not usuario:
            return {"mensaje": "Usuario no encontrado."}

        # Obtener recomendaciones de tipo de texto
        tipo_texto_rec = recomendar_tipo_texto(usuario, db)

        # Obtener un id de temática del usuario
        if usuario.preferencias:
            id_tematica = usuario.preferencias[0].id_tematica
        else:
            id_tematica = 1  # default

        id_tipo_texto = tipo_texto_rec["id_tipo_texto"]
        id_dificultad = 1  # default

        # Construir payload para la API externa
        payload = {
            "id_usuario": id_usuario,
            "id_tipo_texto": id_tipo_texto,
            "id_tematica": id_tematica,
            "id_dificultad": id_dificultad,
            "cantidad": 3  # Número de textos a generar
        }

        # Hacer request al microservicio de generación
        url_externa = f"{API_GENERATION}/contenido/obtener"

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url_externa, params=payload)

            if response.status_code != 200:
                raise Exception(f"Error al obtener textos: {response.text}")

            return response.json()

        except httpx.RequestError as e:
            return {"error": f"Error de conexión con el microservicio: {str(e)}"}
        except Exception as e:
            return {"error": f"Error inesperado: {str(e)}"}
