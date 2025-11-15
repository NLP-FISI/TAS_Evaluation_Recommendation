import httpx
import random
from app.models.usuario import Usuario
from app.models.tematica import Tematica
from app.services.recommendation_tipo_texto_service import recomendar_tipo_texto

API_GENERATION = "https://tas-content-generation.onrender.com"

class TextRecommendationService:
    
    @staticmethod
    async def get_recommendations(id_usuario: int, db):
        """
        Genera 3 textos diversificados según las preferencias del usuario.
        Estrategia de diversificación:
        """
        # Obtener datos del usuario
        usuario = db.query(Usuario).filter(
            Usuario.id_usuario == id_usuario).first()
        if not usuario:
            return {"mensaje": "Usuario no encontrado."}
        
        # Obtener recomendaciones de tipo de texto
        tipo_texto_rec = recomendar_tipo_texto(usuario, db)
        id_tipo_texto = tipo_texto_rec["id_tipo_texto"]
        id_dificultad = 1  # default
        
        # Obtener todas las temáticas disponibles en la BD
        todas_tematicas = db.query(Tematica.id_tematica).all()
        todas_tematicas_ids = [t.id_tematica for t in todas_tematicas]
        
        # Obtener preferencias del usuario
        preferencias_ids = [p.id_tematica for p in usuario.preferencias]
        num_preferencias = len(preferencias_ids)
        
        # Estrategia de selección de temáticas con marcador de preferencia
        tematicas_a_usar = []  # Lista de tuplas (id_tematica, es_preferencia)
        
        if num_preferencias == 0:
            # Sin preferencias: 3 temáticas aleatorias diferentes
            seleccionadas = random.sample(todas_tematicas_ids, min(3, len(todas_tematicas_ids)))
            tematicas_a_usar = [(t, False) for t in seleccionadas]
            
        elif num_preferencias == 1:
            # 1 preferencia: usar la preferencia + 2 aleatorias diferentes
            tematicas_a_usar.append((preferencias_ids[0], True))
            disponibles = [t for t in todas_tematicas_ids if t != preferencias_ids[0]]
            aleatorias = random.sample(disponibles, min(2, len(disponibles)))
            tematicas_a_usar.extend([(t, False) for t in aleatorias])
            
        elif num_preferencias == 2:
            # 2 preferencias: usar ambas + 1 aleatoria diferente
            tematicas_a_usar.extend([(t, True) for t in preferencias_ids])
            disponibles = [t for t in todas_tematicas_ids if t not in preferencias_ids]
            if disponibles:
                tematicas_a_usar.append((random.choice(disponibles), False))
            
        else:  # num_preferencias >= 3
            # 3+ preferencias: elegir 3 aleatorias de sus preferencias sin repetir
            seleccionadas = random.sample(preferencias_ids, 3)
            tematicas_a_usar = [(t, True) for t in seleccionadas]
        
        # Asegurar que tengamos exactamente 3 temáticas (o las que haya disponibles)
        tematicas_a_usar = tematicas_a_usar[:3]
        
        # Hacer las peticiones a la API externa
        resultados = []
        errores = []
        
        url_externa = f"{API_GENERATION}/contenido/obtener"
        
        for idx, (id_tematica, es_preferencia) in enumerate(tematicas_a_usar, 1):
            payload = {
                "id_usuario": id_usuario,
                "id_tipo_texto": id_tipo_texto,
                "id_tematica": id_tematica,
                "id_dificultad": id_dificultad,
                "cantidad": 1  
            }
            
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.get(url_externa, params=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    resultados.append({
                        "texto_numero": idx,
                        "id_tematica": id_tematica,
                        "es_preferencia": es_preferencia,
                        "contenido": data
                    })
                else:
                    errores.append({
                        "texto_numero": idx,
                        "id_tematica": id_tematica,
                        "es_preferencia": es_preferencia,
                        "error": f"Error al obtener texto: {response.text}"
                    })
                    
            except httpx.RequestError as e:
                errores.append({
                    "texto_numero": idx,
                    "id_tematica": id_tematica,
                    "es_preferencia": es_preferencia,
                    "error": f"Error de conexión con el microservicio: {str(e)}"
                })
            except Exception as e:
                errores.append({
                    "texto_numero": idx,
                    "id_tematica": id_tematica,
                    "es_preferencia": es_preferencia,
                    "error": f"Error inesperado: {str(e)}"
                })
        
        # Construir respuesta
        respuesta = {
            "id_usuario": id_usuario,
            "total_textos_solicitados": len(tematicas_a_usar),
            "textos_exitosos": len(resultados),
            "textos_fallidos": len(errores)
        }
        
        if resultados:
            respuesta["textos"] = resultados
        
        if errores:
            respuesta["errores"] = errores
        
        return respuesta