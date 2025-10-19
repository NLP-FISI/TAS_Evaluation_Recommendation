import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    "dbname": "railway",
    "user": "recomendacion01",
    "password": "d2$$4Recom",
    "host": "shortline.proxy.rlwy.net",
    "port": 31885
}

class TextRecommendationService:
    @staticmethod
    async def get_recommendations(id_usuario: int):
        conn = None
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cur = conn.cursor(cursor_factory=RealDictCursor)

            # 1️⃣ Obtener grado del usuario
            cur.execute("""
                SELECT u.id_grado, g.nombre_grado
                FROM usuario u
                JOIN grado g ON u.id_grado = g.id_grado
                WHERE u.id_usuario = %s;
            """, (id_usuario,))
            user_data = cur.fetchone()

            if not user_data:
                return {"mensaje": "Usuario no encontrado."}

            id_grado = user_data["id_grado"]
            nombre_grado = user_data["nombre_grado"]

            # 2️⃣ Obtener textos asociados al grado del usuario
            # (en este caso, filtramos por los tipos de texto que existan para ese grado)
            cur.execute("""
                SELECT 
                    t.id_texto,
                    t.titulo,
                    t.contenido,
                    t.id_tematica,
                    te.nombre_tematica,
                    t.id_tipo_texto,
                    tt.nombre_tipo_texto
                FROM texto t
                JOIN tipo_texto tt ON t.id_tipo_texto = tt.id_tipo_texto
                JOIN tematica te ON t.id_tematica = te.id_tematica
                WHERE t.id_tipo_texto IN (
                    SELECT DISTINCT tx.id_tipo_texto
                    FROM texto tx
                    JOIN tipo_texto ttx ON tx.id_tipo_texto = ttx.id_tipo_texto
                    JOIN usuario u ON u.id_grado = %s
                );
            """, (id_grado,))

            textos = cur.fetchall()

            if not textos:
                return {
                    "mensaje": "No se encontraron textos relacionados con el grado del usuario.",
                    "id_usuario": id_usuario,
                    "grado_usuario": nombre_grado
                }

            return {
                "id_usuario": id_usuario,
                "grado_usuario": nombre_grado,
                "total_textos": len(textos),
                "textos_recomendados": textos
            }

        except Exception as e:
            return {"error": str(e)}

        finally:
            if conn:
                conn.close()
