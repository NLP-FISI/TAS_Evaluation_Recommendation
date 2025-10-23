# app/services/text_recommendation_service.py
import psycopg2
from psycopg2.extras import RealDictCursor
# import requests  # (Descomenta cuando se use la ruta externa)

DB_CONFIG = {
    "dbname": "railway",
    "user": "postgres",
    "password": "YwYQiHoQkwgfhpIJBUVmvqrUKOUMiRBo",
    "host": "crossover.proxy.rlwy.net",
    "port": 57963
}


class TextRecommendationService:
    @staticmethod
    async def get_recommendations(id_usuario: int):
        conn = None
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cur = conn.cursor(cursor_factory=RealDictCursor)

            # 1️⃣ OBTENER DATOS DEL USUARIO (grado, temática, desempeño)
            cur.execute("""
                SELECT 
                    u.id_usuario,
                    u.id_grado,
                    g.nombre_grado,
                    u.id_tematica,
                    te.nombre_tematica,
                    COALESCE(d.promedio, 0) AS puntaje_promedio,
                    COALESCE(d.nivel_actual, 'básico') AS nivel_actual
                FROM usuario AS u
                JOIN grado AS g ON u.id_grado = g.id_grado
                LEFT JOIN tematica AS te ON u.id_tematica = te.id_tematica
                LEFT JOIN desempeno AS d ON u.id_usuario = d.id_usuario
                WHERE u.id_usuario = %s;
            """, (id_usuario,))
            user_data = cur.fetchone()

            if not user_data:
                return {"mensaje": "Usuario no encontrado."}

            # 2️⃣ OBTENER TEXTOS RELEVANTES SEGÚN TEMÁTICA Y NIVEL
            cur.execute("""
                SELECT 
                    t.id_texto,
                    t.titulo,
                    t.contenido,
                    t.id_tematica,
                    te.nombre_tematica,
                    t.id_tipo_texto,
                    tt.nombre_tipo_texto,
                    t.nivel_dificultad
                FROM texto t
                JOIN tematica te ON t.id_tematica = te.id_tematica
                JOIN tipo_texto tt ON t.id_tipo_texto = tt.id_tipo_texto
                WHERE t.id_tematica = %s
                ORDER BY 
                    CASE 
                        WHEN t.nivel_dificultad = %s THEN 1
                        WHEN t.nivel_dificultad = 'medio' THEN 2
                        ELSE 3
                    END;
            """, (user_data["id_tematica"], user_data["nivel_actual"]))

            textos = cur.fetchall()
            if not textos:
                return {"mensaje": "No se encontraron textos para la temática del usuario."}

            # 3️⃣ (FUTURO) ENVIAR DATOS AL MÓDULO EXTERNO PARA GENERAR TEXTO Y PREGUNTAS
            """
            # Ejemplo de integración:
            external_api_url = "http://external-content-generator/api/v1/generate-text"
            payload = {
                "usuario_id": id_usuario,
                "nivel": user_data["nivel_actual"],
                "tematica": user_data["nombre_tematica"],
                "grado": user_data["nombre_grado"]
            }
            response = requests.post(external_api_url, json=payload)
            if response.status_code == 200:
                generated_content = response.json()
            else:
                generated_content = {"error": "No se pudo generar el contenido externo"}
            """

            return {
                "usuario": {
                    "id": user_data["id_usuario"],
                    "grado": user_data["nombre_grado"],
                    "tematica": user_data["nombre_tematica"],
                    "nivel_actual": user_data["nivel_actual"],
                    "puntaje_promedio": user_data["puntaje_promedio"]
                },
                "total_textos": len(textos),
                "textos_recomendados": textos,
                # "contenido_generado": generated_content  # (cuando se conecte el servicio externo)
            }

        except Exception as e:
            return {"error": str(e)}

        finally:
            if conn:
                conn.close()
