# app/services/evaluation_analytics_service.py
# 🔵 NUEVO
from typing import Dict, List
from app.schemas.evaluation_analytics_schemas import (
    EvaluationAnalyticsRequest,
    EvaluationAnalyticsResponse,
)
from app.core.performance_utils import (
    calcular_metricas_por_tipo,
    calcular_metricas_desde_counts,
    determinar_nivel_global,
    generar_recomendaciones_detaladas,
)


class EvaluationAnalyticsService:
    """
    Servicio que encapsula la lógica de análisis para el nuevo endpoint
    (totalmente independiente del servicio existente).
    """

    @staticmethod
    def analyze(data: EvaluationAnalyticsRequest) -> EvaluationAnalyticsResponse:
        # 1) Obtener performance (porcentajes) desde 'answers' o 'counts'
        performance: Dict[str, float] = {}

        if data.answers and len(data.answers) > 0:
            # convertir a lista de dicts (pydantic -> dict)
            answers_simple: List[Dict] = []
            for a in data.answers:
                try:
                    answers_simple.append(a.dict())
                except Exception:
                    # si ya es dict
                    answers_simple.append(a)
            performance = calcular_metricas_por_tipo(answers_simple)

        elif data.counts:
            performance = calcular_metricas_desde_counts(data.counts)

        else:
            # Si no hay datos suficientes, devolver ceros vacíos
            performance = {"literal": 0.0, "inferencial": 0.0, "critico": 0.0}

        # 2) Nivel global
        overall_level = determinar_nivel_global(performance)

        # 3) Recomendaciones detalladas
        recommendations = generar_recomendaciones_detaladas(performance)

        # 4) Construir respuesta
        return EvaluationAnalyticsResponse(
            student_id=data.student_id,
            performance=performance,
            overall_level=overall_level,
            recommendations=recommendations,
            message="Análisis completado correctamente."
        )
