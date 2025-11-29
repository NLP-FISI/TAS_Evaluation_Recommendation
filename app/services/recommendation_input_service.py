from app.models.usuario import Usuario
from app.models.pregunta import Pregunta
import re


class RecommendationInputService:
    """
    Servicio que genera textos de prueba de entrada (fase 1 y fase 2)
    de forma temporal (hardcodeado).
    """

    @staticmethod
    def _strip_html_tags(html_content: str) -> str:
        """Elimina todas las etiquetas HTML y retorna solo el texto plano."""
        clean = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL)
        clean = re.sub(r'<script[^>]*>.*?</script>', '', clean, flags=re.DOTALL)
        clean = re.sub(r'<[^>]+>', '', clean)
        clean = re.sub(r'\n\s*\n', '\n\n', clean)
        clean = re.sub(r' +', ' ', clean)
        return clean.strip()

    @staticmethod
    def get_input_texts(id_usuario: int, db):
        # Buscar usuario
        usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
        if not usuario:
            return {"mensaje": "Usuario no encontrado"}

        # Obtener datos relevantes
        edad = usuario.edad
        grado = usuario.grado.nombre_grado if usuario.grado else "Sin grado"
        preferencias = [t.nombre_tematica for t in usuario.preferencias] if usuario.preferencias else ["General"]

        # Obtener textos de diagnóstico desde la base de datos (ID 1 y 2)
        texto_ids = [1, 2]
        
        # Consultar preguntas asociadas a estos textos
        preguntas = (
            db.query(Pregunta)
            .filter(Pregunta.id_texto.in_(texto_ids))
            .order_by(Pregunta.id_texto, Pregunta.id_pregunta)
            .all()
        )
        
        # Agrupar preguntas por texto
        textos_dict = {}
        for pregunta in preguntas:
            texto = pregunta.texto
            if not texto:
                continue
                
            if texto.id_texto not in textos_dict:
                # Detectar si tiene HTML
                has_html = bool(texto.contenido and ('<' in texto.contenido and '>' in texto.contenido))
                
                # Convertir a texto plano si tiene HTML
                content = texto.contenido or ""
                if has_html:
                    content = RecommendationInputService._strip_html_tags(content)
                
                textos_dict[texto.id_texto] = {
                    "id_texto": texto.id_texto,
                    "titulo": texto.titulo or f"Texto {texto.id_texto}",
                    "contenido": content,
                    "preguntas": []
                }
            
            # Construir alternativas
            alternativas = [
                {
                    "id_alternativa": alt.id_alternativa,
                    "contenido": alt.contenido
                }
                for alt in pregunta.alternativas
            ]
            
            # Agregar pregunta
            textos_dict[texto.id_texto]["preguntas"].append({
                "id_pregunta": pregunta.id_pregunta,
                "contenido": pregunta.contenido,
                "id_dificultad": pregunta.id_dificultad,
                "id_tipo_pregunta": pregunta.id_tipo_pregunta,
                "alternativas": alternativas
            })
        
        # Convertir dict a lista ordenada
        textos_lista = [textos_dict[tid] for tid in sorted(textos_dict.keys())]
        
        # Crear fases
        fase_1 = {
            "fase": "Fase 1",
            "descripcion": "Preguntas literal e inferencial básica",
            "textos_obtenidos": 1,
            "textos": [textos_lista[0]] if len(textos_lista) > 0 else []
        }

        fase_2 = {
            "fase": "Fase 2",
            "descripcion": "Preguntas literal, inferencial intermedio y crítica",
            "textos_obtenidos": 1,
            "textos": [textos_lista[1]] if len(textos_lista) > 1 else []
        }

        # Armar la respuesta final
        return {
            "usuario": {
                "id_usuario": usuario.id_usuario,
                "nombre": f"{usuario.nombre_usuario} {usuario.apellido_usuario}",
                "edad": edad,
                "grado": grado,
                "preferencias": preferencias
            },
            "recomendaciones": [fase_1, fase_2]
        }

