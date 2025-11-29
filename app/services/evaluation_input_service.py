# File: app/services/evaluation_input_service.py
from typing import List
from app.schemas.evaluation_schemas import EvaluationInputRequest, EvaluationInputResponse


class EvaluationInputService:
    @staticmethod
    def evaluate_student(data: EvaluationInputRequest) -> EvaluationInputResponse:
        """
        Lógica de negocio para evaluar al estudiante al inicio.
        (Ejemplo simple, luego se conecta con BD y modelos más complejos).
        """

        # Simulación de cálculo de nivel inicial
        if data.grade_level <= 3:
            level = "básico"
            texts = ["Cuento: El gato curioso", "Historia: La pelota perdida"]
        else:
            level = "intermedio"
            texts = ["Aventura: Viaje al espacio", "Ciencia: Los volcanes"]

        return EvaluationInputResponse(
            student_id=data.student_id,
            initial_level=level,
            recommended_texts=texts,
            message="Evaluación inicial completada exitosamente."
        )
