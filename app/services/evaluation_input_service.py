# File: app/services/evaluation_input_service.py
from typing import List, Dict, Any
from app.schemas.evaluation_schemas import EvaluationInputRequest, EvaluationInputResponse


class EvaluationInputService:
    # Mapping de niveles de lectura basado en grado escolar
    GRADE_LEVEL_MAPPING = {
        2: {"level": "básico", "complexity": 1},
        3: {"level": "básico", "complexity": 2},
        4: {"level": "intermedio", "complexity": 1},
        5: {"level": "intermedio", "complexity": 2},
        6: {"level": "avanzado", "complexity": 1}
    }
    
    # Textos organizados por nivel, complejidad y preferencias
    TEXT_LIBRARY = {
        "básico": {
            1: {  # Complejidad 1
                "animales": [
                    "Cuento: El gato curioso",
                    "Historia: La tortuga y la liebre",
                    "Fábula: El ratón y el león"
                ],
                "aventuras": [
                    "Historia: La pelota perdida",
                    "Cuento: El tesoro del jardín",
                    "Aventura: El viaje en globo"
                ],
                "ciencia": [
                    "Historia: Las plantas mágicas",
                    "Cuento: La lluvia de colores",
                    "Experimento: El arcoíris en casa"
                ],
                "default": [
                    "Cuento: El gato curioso",
                    "Historia: La pelota perdida",
                    "Fábula: Los tres cerditos"
                ]
            },
            2: {  # Complejidad 2
                "animales": [
                    "Historia: El bosque encantado",
                    "Cuento: La familia de osos",
                    "Aventura: Safari en África"
                ],
                "aventuras": [
                    "Historia: El pirata bueno",
                    "Cuento: La isla misteriosa",
                    "Aventura: En busca del tesoro"
                ],
                "ciencia": [
                    "Historia: Los dinosaurios amigables",
                    "Cuento: El sistema solar",
                    "Experimento: Volcanes caseros"
                ],
                "default": [
                    "Historia: El bosque encantado",
                    "Cuento: El pirata bueno",
                    "Historia: Los dinosaurios amigables"
                ]
            }
        },
        "intermedio": {
            1: {  # Complejidad 1
                "animales": [
                    "Novela: La selva perdida",
                    "Historia: Los animales del mundo",
                    "Aventura: Rescate en la montaña"
                ],
                "aventuras": [
                    "Aventura: Viaje al espacio",
                    "Historia: Los exploradores valientes",
                    "Novela: El misterio del castillo"
                ],
                "ciencia": [
                    "Ciencia: Los volcanes",
                    "Historia: Los inventos geniales",
                    "Experimento: La química divertida"
                ],
                "default": [
                    "Aventura: Viaje al espacio",
                    "Ciencia: Los volcanes",
                    "Historia: Los exploradores valientes"
                ]
            },
            2: {  # Complejidad 2
                "animales": [
                    "Novela: El reino animal",
                    "Historia: Especies en peligro",
                    "Aventura: Expedición amazónica"
                ],
                "aventuras": [
                    "Novela: La máquina del tiempo",
                    "Historia: Grandes descubrimientos",
                    "Aventura: Misión espacial"
                ],
                "ciencia": [
                    "Ciencia: El universo infinito",
                    "Historia: Científicos famosos",
                    "Experimento: Física asombrosa"
                ],
                "default": [
                    "Novela: La máquina del tiempo",
                    "Ciencia: El universo infinito",
                    "Historia: Grandes descubrimientos"
                ]
            }
        },
        "avanzado": {
            1: {  # Complejidad 1
                "animales": [
                    "Novela: Ecosistemas en equilibrio",
                    "Historia: Evolución de las especies",
                    "Ensayo: Conservación animal"
                ],
                "aventuras": [
                    "Novela: Travesías épicas",
                    "Historia: Exploradores legendarios",
                    "Aventura: Civilizaciones perdidas"
                ],
                "ciencia": [
                    "Ciencia: Avances tecnológicos",
                    "Historia: Revolución científica",
                    "Ensayo: El futuro de la humanidad"
                ],
                "default": [
                    "Novela: Travesías épicas",
                    "Ciencia: Avances tecnológicos",
                    "Historia: Revolución científica"
                ]
            }
        }
    }

    @staticmethod
    def evaluate_student(data: EvaluationInputRequest) -> EvaluationInputResponse:
        """
        Algoritmo mejorado para la asignación automática del nivel inicial.
        Considera el grado escolar, preferencias y complejidad apropiada.
        """
        
        # Validar grado escolar
        if data.grade_level < 2 or data.grade_level > 6:
            return EvaluationInputResponse(
                student_id=data.student_id,
                initial_level="básico",
                recommended_texts=EvaluationInputService.TEXT_LIBRARY["básico"][1]["default"],
                message="Grado escolar fuera del rango válido (2-6). Asignado nivel básico por defecto."
            )
        
        # Obtener nivel y complejidad basado en el grado
        level_info = EvaluationInputService.GRADE_LEVEL_MAPPING[data.grade_level]
        assigned_level = level_info["level"]
        complexity = level_info["complexity"]
        
        # Obtener textos recomendados basados en preferencias
        recommended_texts = EvaluationInputService._get_recommended_texts(
            assigned_level, complexity, data.preferences
        )
        
        # Generar mensaje personalizado
        message = EvaluationInputService._generate_personalized_message(
            assigned_level, data.grade_level, data.preferences
        )
        
        return EvaluationInputResponse(
            student_id=data.student_id,
            initial_level=assigned_level,
            recommended_texts=recommended_texts,
            message=message
        )
    
    @staticmethod
    def _get_recommended_texts(level: str, complexity: int, preferences: List[str]) -> List[str]:
        """
        Obtiene textos recomendados basados en nivel, complejidad y preferencias.
        """
        texts_by_level = EvaluationInputService.TEXT_LIBRARY.get(level, {})
        texts_by_complexity = texts_by_level.get(complexity, {})
        
        if not texts_by_complexity:
            # Fallback a complejidad 1 si no existe la complejidad solicitada
            texts_by_complexity = texts_by_level.get(1, {})
        
        if not preferences:
            # Sin preferencias específicas, usar textos por defecto
            return texts_by_complexity.get("default", [
                "Texto: Lectura general",
                "Historia: Contenido adaptado",
                "Cuento: Historia interesante"
            ])
        
        # Combinar textos según preferencias
        recommended = []
        for preference in preferences[:2]:  # Máximo 2 preferencias para evitar lista muy larga
            preference_texts = texts_by_complexity.get(preference.lower(), [])
            recommended.extend(preference_texts[:2])  # Máximo 2 textos por preferencia
        
        # Si no se encontraron textos para las preferencias, usar por defecto
        if not recommended:
            recommended = texts_by_complexity.get("default", [])
        
        # Eliminar duplicados manteniendo el orden
        seen = set()
        unique_texts = []
        for text in recommended:
            if text not in seen:
                seen.add(text)
                unique_texts.append(text)
        
        return unique_texts[:4]  # Máximo 4 textos recomendados
    
    @staticmethod
    def _generate_personalized_message(level: str, grade_level: int, preferences: List[str]) -> str:
        """
        Genera un mensaje personalizado basado en el nivel asignado y preferencias.
        """
        base_message = f"Evaluación inicial completada. Nivel asignado: {level} "
        base_message += f"(apropiado para {grade_level}° grado)"
        
        if preferences:
            preferences_text = ", ".join(preferences[:3])  # Máximo 3 preferencias en el mensaje
            base_message += f". Textos seleccionados considerando tus intereses en: {preferences_text}"
        
        base_message += ". ¡Empecemos a leer!"
        
        return base_message
