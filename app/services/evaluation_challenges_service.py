#app/services/evaluation_challenges_service.py

import math
# Se importa desde el nuevo archivo de esquemas
from app.schemas.evaluation_challenges import RetoParaEvaluar, ResultadoEvaluacion, UsuarioData, RetoResultadoEnum
from app.models.reto import Reto
from app.models.juego import Juego # Suponiendo que existe un modelo Juego
from sqlalchemy import or_
from sqlalchemy.orm import Session

class EvaluationChallengeService:
    """
    La lógica interna no cambia, solo los nombres de los campos que consume.
    """
    
    @staticmethod
    def _calculate_new_elo_ratings(rating_a: int, rating_b: int, score_a: float, k_factor: int = 32) -> tuple[int, int]:
        expected_a = 1 / (1 + math.pow(10, (rating_b - rating_a) / 400))
        expected_b = 1 / (1 + math.pow(10, (rating_a - rating_b) / 400))
        
        score_b = 1.0 - score_a
        
        new_rating_a_float = rating_a + k_factor * (score_a - expected_a)
        new_rating_b_float = rating_b + k_factor * (score_b - expected_b)
        
        return int(round(new_rating_a_float)), int(round(new_rating_b_float))

    @staticmethod
    def _determinar_resultado_reto(reto_input: RetoParaEvaluar) -> tuple[RetoResultadoEnum, int | None]:
        retador = reto_input.retador
        contrincante = reto_input.contrincante

        if retador.respuestas_correctas > contrincante.respuestas_correctas:
            return RetoResultadoEnum.victoria_retador, retador.id_usuario
        elif contrincante.respuestas_correctas > retador.respuestas_correctas:
            return RetoResultadoEnum.victoria_contrincante, contrincante.id_usuario
        else:
            if retador.tiempo_total_seg < contrincante.tiempo_total_seg:
                return RetoResultadoEnum.victoria_retador, retador.id_usuario
            elif contrincante.tiempo_total_seg < retador.tiempo_total_seg:
                return RetoResultadoEnum.victoria_contrincante, contrincante.id_usuario
            else:
                return RetoResultadoEnum.empate, None

    @staticmethod
    def _calcular_puntuacion_rendimiento(respuestas_correctas: int, tiempo_total_seg: int) -> float:
        """
        Calcula una puntuación de rendimiento simple.
        Más correctas es mejor, menos tiempo es mejor.
        """
        if tiempo_total_seg == 0:
            return respuestas_correctas * 10.0  # Evitar división por cero
        
        # Penalización por tiempo: más tiempo reduce la puntuación.
        # El factor 100 es para que el tiempo no domine sobre las respuestas correctas.
        puntuacion = (respuestas_correctas * 10) - (tiempo_total_seg / 100.0)
        return max(0, puntuacion) # Asegurar que la puntuación no sea negativa

    @classmethod
    def procesar_evaluacion_reto(
        cls, 
        reto_input: RetoParaEvaluar, 
        retador_data: UsuarioData, 
        contrincante_data: UsuarioData,
        racha_victorias_retador: int,
        racha_derrotas_retador: int,
        racha_victorias_contrincante: int,
        racha_derrotas_contrincante: int
    ) -> ResultadoEvaluacion:
        
        resultado, id_ganador = cls._determinar_resultado_reto(reto_input)

        cambio_rating_retador, cambio_rating_contrincante = cls._calcular_cambio_rating(
            retador_data.puntos, contrincante_data.puntos, resultado
        )

        bonus_retador = 0
        bonus_contrincante = 0

        if resultado == RetoResultadoEnum.victoria_retador:
            bonus_retador = cls._calcular_bonus_racha(
                racha_victorias_retador, 
                racha_derrotas_retador
            )
        elif resultado == RetoResultadoEnum.victoria_contrincante:
            bonus_contrincante = cls._calcular_bonus_racha(
                racha_victorias_contrincante,
                racha_derrotas_contrincante
            )

        cambio_rating_retador += bonus_retador
        cambio_rating_contrincante += bonus_contrincante

        # Calcular puntuaciones de rendimiento para generar el mensaje
        puntuacion_retador = cls._calcular_puntuacion_rendimiento(
            reto_input.retador.respuestas_correctas, reto_input.retador.tiempo_total_seg
        )
        puntuacion_contrincante = cls._calcular_puntuacion_rendimiento(
            reto_input.contrincante.respuestas_correctas, reto_input.contrincante.tiempo_total_seg
        )

        if resultado == RetoResultadoEnum.victoria_retador:
            mensaje_personalizado = cls._generar_mensaje_personalizado(
                puntuacion_ganador=puntuacion_retador,
                puntuacion_perdedor=puntuacion_contrincante,
                racha_victorias_ganador=racha_victorias_retador,
                racha_derrotas_ganador=racha_derrotas_retador
            )
        elif resultado == RetoResultadoEnum.victoria_contrincante:
            mensaje_personalizado = cls._generar_mensaje_personalizado(
                puntuacion_ganador=puntuacion_contrincante,
                puntuacion_perdedor=puntuacion_retador,
                racha_victorias_ganador=racha_victorias_contrincante,
                racha_derrotas_ganador=racha_derrotas_contrincante
            )
        else: # Empate
            mensaje_personalizado = "¡Empate! 🤝"

        return ResultadoEvaluacion(
            id_ganador=id_ganador,
            id_retador=reto_input.retador.id_usuario,
            rating_anterior_retador=retador_data.puntos,
            rating_nuevo_retador=retador_data.puntos + cambio_rating_retador,
            variacion_retador=cambio_rating_retador,
            id_contrincante=reto_input.contrincante.id_usuario,
            rating_anterior_contrincante=contrincante_data.puntos,
            rating_nuevo_contrincante=contrincante_data.puntos + cambio_rating_contrincante,
            variacion_contrincante=cambio_rating_contrincante,
            mensaje=f"El resultado es: {resultado.value}",
            mensaje_personalizado=mensaje_personalizado
        )

    @classmethod
    def _calcular_cambio_rating(cls, rating_retador: int, rating_contrincante: int, resultado: RetoResultadoEnum) -> tuple[int, int]:
        """
        Calcula la variación de puntos Elo para ambos jugadores.
        """
        if resultado == RetoResultadoEnum.victoria_retador:
            score_a = 1.0
        elif resultado == RetoResultadoEnum.victoria_contrincante:
            score_a = 0.0
        else: # Empate
            score_a = 0.5

        nuevo_rating_retador, nuevo_rating_contrincante = cls._calculate_new_elo_ratings(
            rating_retador, rating_contrincante, score_a
        )

        variacion_retador = nuevo_rating_retador - rating_retador
        variacion_contrincante = nuevo_rating_contrincante - rating_contrincante

        return variacion_retador, variacion_contrincante
    
    @classmethod
    def _generar_mensaje_personalizado(cls, puntuacion_ganador: float, puntuacion_perdedor: float, racha_victorias_ganador: int, racha_derrotas_ganador: int) -> str:
        """
        Genera un mensaje de victoria basado en el rendimiento, adaptado para niños.
        El orden de las condiciones es de más específico a más general.
        """
        diferencia_puntuacion = abs(puntuacion_ganador - puntuacion_perdedor)

        # 1. Condición de remontada (muy específica)
        if racha_victorias_ganador == 0 and racha_derrotas_ganador >= 3:
            return "¡De vuelta al juego! 🚀"

        # 2. Condiciones por diferencia de rendimiento
        if diferencia_puntuacion <= 1.0: # Puntuaciones casi idénticas
            return "¡Por un pelo! ¡Qué final tan reñido! 🤏"
        
        if diferencia_puntuacion > 40:
            return "¡Imparable! 🔥"
        
        # 3. Condiciones por puntuación alta del ganador
        if puntuacion_ganador > 80:
            return "¡Súper Estrella! 🌟"
        
        # 4. Otras condiciones de rendimiento
        if diferencia_puntuacion < 5:
            return "¡Casi iguales! 😮"

        if puntuacion_ganador > 78.8 and diferencia_puntuacion > 19.9:
            return "¡Qué rápido! ⚡️"
        
        # 5. Mensaje por defecto
        return "¡Muy bien! 👍"
    
    @classmethod
    def _calcular_bonus_racha(cls, racha_victorias: int, racha_derrotas: int) -> int:
        """
        Calcula un bonus de puntos basado en las rachas.
        """
        if racha_victorias >= 3:
            # Bonus "On Fire": +3, +4, +5...
            return min(racha_victorias, 10)  # Un tope para que no sea infinito
        
        if racha_derrotas >= 3:
            # Bonus "Remontada": Gana más puntos para romper la mala racha.
            return 5 + min(racha_derrotas, 10)
            
        return 0

    @classmethod
    def _get_user_streak(cls, user_id: int, db: Session) -> tuple[int, int]:
        """
        Calcula la racha de victorias y derrotas de un usuario consultando la BD.
        """
        # Subconsulta para obtener los id_juego de los retos del usuario
        retos_usuario_ids = db.query(Reto.id_juego).filter(
            or_(Reto.id_usuario_retador == user_id, Reto.id_usuario_contrincante == user_id)
        )

        # Consulta principal uniendo Reto y Juego
        ultimos_retos = db.query(Reto).join(Juego, Reto.id_juego == Juego.id_juego).filter(
            Reto.id_juego.in_(retos_usuario_ids),
            Reto.estado == 'finalizado' # Asumimos que este es el estado de un reto completado
        ).order_by(Juego.fecha_creacion.desc()).limit(20).all()

        if not ultimos_retos:
            return 0, 0

        racha_victorias = 0
        racha_derrotas = 0
        
        # El primer reto de la lista es el más reciente
        if ultimos_retos[0].ganador == user_id:
            # El usuario ganó el último reto, contamos la racha de victorias
            for reto in ultimos_retos:
                if reto.ganador == user_id:
                    racha_victorias += 1
                else:
                    break
        elif ultimos_retos[0].ganador is not None:
            # El usuario perdió, contamos la racha de derrotas
            for reto in ultimos_retos:
                if reto.ganador is not None and reto.ganador != user_id:
                    racha_derrotas += 1
                else:
                    break
        
        return racha_victorias, racha_derrotas