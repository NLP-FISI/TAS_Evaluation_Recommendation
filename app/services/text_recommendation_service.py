import psycopg2
from psycopg2.extras import RealDictCursor

class TextRecommendationService:

    @staticmethod
    async def get_recommended_texts(id_usuario: int):
        """
        Lógica que filtra textos basados en el grado del usuario y los tipos de texto correspondientes.
        """

        # 🔹 1. Conectarse a la base de datos (Railway)
        conn = psycopg2.connect(
            host="shortline.proxy.rlwy.net",
            port="31885",
            user="recomendacion01",
            password="d2$$4Recom",
            database="railway"
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # 🔹 2. Obtener el grado del usuario
        cur.execute("SELECT ID_Grado FROM Usuario WHERE ID_Usuario = %s;", (id_usuario,))
        grado_row = cur.fetchone()

        if not grado_row:
            cur.close()
            conn.close()
            return {"mensaje": "Usuario no encontrado o sin grado registrado."}

        grado = grado_row["ID_Grado"]

        # 🔹 3. Definir tipos de texto según el grado (regla simulada)
        tipos_por_grado = {
            2: [1, 3],  # Narrativo e Instructivo
            3: [1, 2],  # Narrativo y Expositivo
            4: [2, 3],  # Expositivo e Instructivo
            5: [2],     # Expositivo
            6: [4]      # Argumentativo (por ejemplo)
        }

        tipos_texto = tipos_por_grado.get(grado, [1])

        # 🔹 4. Obtener textos según los tipos (aunque la BD esté vacía)
        cur.execute("""
            SELECT t.ID_Texto, t.Título, t.Contenido, te.Nombre_Tematica, tt.Nombre_Tipo_Texto
            FROM Texto t
            JOIN Tematica te ON t.ID_Tematica = te.ID_Tematica
            JOIN Tipo_Texto tt ON t.ID_Tipo_Texto = tt.ID_Tipo_Texto
            WHERE t.ID_Tipo_Texto = ANY(%s);
        """, (tipos_texto,))

        textos = cur.fetchall()

        cur.close()
        conn.close()

        # 🔹 5. Retornar la respuesta
        return {
            "id_usuario": id_usuario,
            "grado": grado,
            "tipos_texto": tipos_texto,
            "total_textos_encontrados": len(textos),
            "textos": textos
        }
