import psycopg2
from psycopg2.extras import RealDictCursor

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

            # 1 Obtener datos del usuario (grado y temática)
            cur.execute("""
                SELECT 
                    u.id_grado,
                    g.nombre_grado,
                    u.id_tematica,
                    te.nombre_tematica
                FROM usuario AS u
                JOIN grado AS g ON u.id_grado = g.id_grado
                LEFT JOIN tematica AS te ON u.id_tematica = te.id_tematica
                WHERE u.id_usuario = %s;
            """, (id_usuario,))
            user_data = cur.fetchone()

            if not user_data:
                return {"mensaje": "Usuario no encontrado."}

            id_grado = user_data["id_grado"]
            nombre_grado = user_data["nombre_grado"]
            id_tematica = user_data["id_tematica"]
            nombre_tematica = user_data["nombre_tematica"]

            if not id_tematica:
                return {"mensaje": "El usuario no tiene asignada una temática."}

            # 2 Obtener textos que coincidan con la temática del usuario
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
                JOIN tematica te ON t.id_tematica = te.id_tematica
                JOIN tipo_texto tt ON t.id_tipo_texto = tt.id_tipo_texto
                WHERE t.id_tematica = %s;
            """, (id_tematica,))

            textos = cur.fetchall()

            if not textos:
                return {"mensaje": "No se encontraron textos para la temática del usuario."}

            return {
                "id_usuario": id_usuario,
                "grado_usuario": nombre_grado,
                "tematica_usuario": nombre_tematica,
                "total_textos": len(textos),
                "textos_recomendados": textos
            }

        except Exception as e:
            return {"error": str(e)}

        finally:
            if conn:
                conn.close()
