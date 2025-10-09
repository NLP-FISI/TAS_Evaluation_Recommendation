import math
from app.schemas.evaluation_schemas import RetoParaEvaluar, ResultadoEvaluacion, UsuarioData, RetoResultadoEnum

class EvaluationChallengeService:
    """
    Clase de servicio que encapsula toda la lógica de negocio
    para la evaluación de retos competitivos.
    
    Los métodos son estáticos porque no dependen del estado de una instancia.
    """
    
    @staticmethod
    def _calculate_new_elo_ratings(rating_a: int, rating_b: int, score_a: float, k_factor: int = 32) -> tuple[int, int]:
        """
        Calcula los nuevos ratings ELO y los devuelve como enteros.
        """
        expected_a = 1 / (1 + math.pow(10, (rating_b - rating_a) / 400))
        expected_b = 1 / (1 + math.pow(10, (rating_a - rating_b) / 400))
        
        score_b = 1.0 - score_a
        
        new_rating_a_float = rating_a + k_factor * (score_a - expected_a)
        new_rating_b_float = rating_b + k_factor * (score_b - expected_b)
        
        new_rating_a_int = int(round(new_rating_a_float))
        new_rating_b_int = int(round(new_rating_b_float))
        
        return new_rating_a_int, new_rating_b_int

    @staticmethod
    def _determinar_resultado_reto(reto_input: RetoParaEvaluar) -> tuple[RetoResultadoEnum, int | None]:
        """
        Aplica la lógica de negocio para determinar al ganador.
        """
        retador = reto_input.retador
        contrincante = reto_input.contrincante

        if retador.respuestas_correctas > contrincante.respuestas_correctas:
            return (RetoResultadoEnum.victoria_retador, retador.id_usuario)
        elif contrincante.respuestas_correctas > retador.respuestas_correctas:
            return (RetoResultadoEnum.victoria_contrincante, contrincante.id_usuario)
        else:
            if retador.tiempo_total_seg < contrincante.tiempo_total_seg:
                return (RetoResultadoEnum.victoria_retador, retador.id_usuario)
            elif contrincante.tiempo_total_seg < retador.tiempo_total_seg:
                return (RetoResultadoEnum.victoria_contrincante, contrincante.id_usuario)
            else:
                return (RetoResultadoEnum.empate, None)

    @classmethod
    def procesar_evaluacion_reto(cls, reto_input: RetoParaEvaluar, retador_data: UsuarioData, contrincante_data: UsuarioData) -> ResultadoEvaluacion:
        """
        Método principal que orquesta el proceso de evaluación de un reto.
        """
        resultado, id_ganador = cls._determinar_resultado_reto(reto_input)
        
        elo_retador_actual = retador_data.puntaje_elo
        elo_contrincante_actual = contrincante_data.puntaje_elo
        
        if resultado == RetoResultadoEnum.victoria_retador:
            score_retador = 1.0
        elif resultado == RetoResultadoEnum.victoria_contrincante:
            score_retador = 0.0
        else:
            score_retador = 0.5
            
        nuevo_elo_retador, nuevo_elo_contrincante = cls._calculate_new_elo_ratings(
            rating_a=elo_retador_actual,
            rating_b=elo_contrincante_actual,
            score_a=score_retador
        )
        
        return ResultadoEvaluacion(
            id_ganador=id_ganador,
            id_retador=retador_data.id,
            rating_anterior_retador=elo_retador_actual,
            rating_nuevo_retador=nuevo_elo_retador,
            variacion_retador=nuevo_elo_retador - elo_retador_actual,
            id_contrincante=contrincante_data.id,
            rating_anterior_contrincante=elo_contrincante_actual,
            rating_nuevo_contrincante=nuevo_elo_contrincante,
            variacion_contrincante=nuevo_elo_contrincante - elo_contrincante_actual,
            mensaje=f"Evaluación completada. Ganador: {id_ganador if id_ganador else 'Empate'}."
        )