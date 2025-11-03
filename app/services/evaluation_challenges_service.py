#app/services/evaluation_challenges_service.py

import math
# Se importa desde el nuevo archivo de esquemas
from app.schemas.evaluation_challenges import RetoParaEvaluar, ResultadoEvaluacion, UsuarioData, RetoResultadoEnum

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

    @classmethod
    def procesar_evaluacion_reto(cls, reto_input: RetoParaEvaluar, retador_data: UsuarioData, contrincante_data: UsuarioData) -> ResultadoEvaluacion:
        resultado, id_ganador = cls._determinar_resultado_reto(reto_input)

        cambio_rating_retador, cambio_rating_contrincante = cls._calcular_cambio_rating(
            retador_data.puntos, contrincante_data.puntos, resultado
        )

        # --- INICIO DE LA NUEVA LÓGICA ---

        # 1. Calcular bonus por rachas
        bonus_retador = 0
        bonus_contrincante = 0

        if resultado == RetoResultadoEnum.victoria_retador:
            bonus_retador = cls._calcular_bonus_racha(
                reto_input.retador.racha_victorias, 
                reto_input.retador.racha_derrotas
            )
        elif resultado == RetoResultadoEnum.victoria_contrincante:
            bonus_contrincante = cls._calcular_bonus_racha(
                reto_input.contrincante.racha_victorias,
                reto_input.contrincante.racha_derrotas
            )

        # Aplicar bonus al ganador
        cambio_rating_retador += bonus_retador
        cambio_rating_contrincante += bonus_contrincante

        # 2. Generar mensaje personalizado
        diff_correctas = abs(reto_input.retador.respuestas_correctas - reto_input.contrincante.respuestas_correctas)
        diff_tiempo = abs(reto_input.retador.tiempo_total_seg - reto_input.contrincante.tiempo_total_seg)
        
        mensaje_personalizado = cls._generar_mensaje_personalizado(resultado, diff_correctas, diff_tiempo)

        # --- FIN DE LA NUEVA LÓGICA ---

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
            mensaje_personalizado=mensaje_personalizado  # <-- Nuevo campo
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

        # --- ESTA ES LA PARTE CORREGIDA ---
        # Llamamos a la función una sola vez y desempaquetamos la tupla
        nuevo_rating_retador, nuevo_rating_contrincante = cls._calculate_new_elo_ratings(
            rating_retador, rating_contrincante, score_a
        )

        # Calculamos la diferencia (variación) para cada uno
        variacion_retador = nuevo_rating_retador - rating_retador
        variacion_contrincante = nuevo_rating_contrincante - rating_contrincante

        return variacion_retador, variacion_contrincante
    
    @classmethod
    def _generar_mensaje_personalizado(cls, resultado: RetoResultadoEnum, diff_correctas: int, diff_tiempo: float) -> str:
        """
        Genera un mensaje de victoria basado en el rendimiento.
        """
        if resultado == RetoResultadoEnum.empate:
            return "¡Empate reñido!"

        # Mensajes para el ganador
        if diff_correctas > 3:
            return "¡Dominante!"
        if diff_tiempo > 60:
            return "¡Victoria aplastante!"
        if diff_correctas > 1:
            return "¡Victoria sólida!"
        if diff_tiempo < 10:
            return "¡Final de infarto!"
        
        return "¡Buen trabajo!"
    
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