"""
Servicio para manejar la lógica de negocio del diagnóstico inicial (Etapa 1).
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from pydantic import BaseModel, Field
from typing import List

# Modelos importados del paquete app.models
from app.models.pregunta import Pregunta
from app.models.alternativa import Alternativa
from app.models.resultado_diagnostico import ResultadoDiagnostico
from app.models.texto import Texto
from app.models.usuario import Usuario


class Answer(BaseModel):
    """Modelo para representar una respuesta enviada por el estudiante."""
    question_id: int = Field(..., description="ID de la pregunta respondida.")
    alternative_id: int = Field(..., description="ID de la alternativa seleccionada.")


# --- Esquemas para la Etapa 1 (F-02.A) ---
class DiagnosticStage1Request(BaseModel):
    """Solicitud para la Etapa 1 del diagnóstico."""
    student_id: str = Field(..., description="ID único del estudiante (puede ser string)")
    answers: List[Answer] = Field(..., min_items=2, max_items=2,
                                  description="Lista con exactamente 2 respuestas")


class DiagnosticStage1Response(BaseModel):
    """Respuesta de la Etapa 1 del diagnóstico."""
    student_id: str
    decision: str = Field(..., description="'CONTINUAR' o 'FINALIZAR'")
    correct_answers_count: int = Field(..., ge=0, le=2,
                                       description="Número de respuestas correctas (0, 1 o 2)")
    message: str


# --- Esquemas para la Etapa 2 (F-02.B) ---
class DiagnosticStage2Request(BaseModel):
    """Solicitud para la Etapa 2 del diagnóstico."""
    student_id: str = Field(..., description="ID único del estudiante (puede ser string)")
    answers: List[Answer] = Field(..., min_items=3, max_items=3,
                                  description="Lista con exactamente 3 respuestas")


class DiagnosticStage2Response(BaseModel):
    """Respuesta de la Etapa 2 del diagnóstico."""
    student_id: str
    correct_answers_count: int = Field(..., ge=0, le=3,
                                       description="Número de respuestas correctas (0, 1, 2 o 3)")
    message: str


# --- Nuevos esquemas para F-03 ---
class LevelAssignmentRequest(BaseModel):
    """Solicitud para iniciar la asignación de nivel (F-03)."""
    student_id: str = Field(..., description="ID del estudiante a calificar.")


class LevelAssignmentResponse(BaseModel):
    """Respuesta de la asignación de nivel (F-03)."""
    student_id: str
    assigned_level_label: str = Field(..., description="Etiqueta de nivel asignado (ej. '4to Grado')")
    assigned_level_grade: int = Field(..., description="ID del grado de competencia asignado (ej. 4)")
    message: str


# --- Servicio principal ---
class DiagnosticService:
    """Contiene la lógica de negocio del diagnóstico (Etapa 1)."""

    @staticmethod
    def process_stage1(db: Session, data: DiagnosticStage1Request) -> DiagnosticStage1Response:
        """
        Procesa las respuestas de la Etapa 1 del diagnóstico.
        Verifica las respuestas, guarda los resultados y determina si continuar.
        """
        # 1. Verificar que el estudiante exista
        db_user = db.query(Usuario).filter(Usuario.student_id == data.student_id).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Estudiante con id '{data.student_id}' no encontrado."
            )

        # 2. Verificar cantidad de respuestas
        if len(data.answers) != 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Se deben enviar exactamente 2 respuestas para la Etapa 1."
            )

        correct_answers_count = 0
        results_to_save = []

        # 3. Procesar cada respuesta
        for answer in data.answers:
            chosen_alternative = db.query(Alternativa).filter(
                Alternativa.id_alternativa == answer.alternative_id,
                Alternativa.id_pregunta == answer.question_id
            ).first()

            if not chosen_alternative:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Alternativa {answer.alternative_id} no encontrada para la pregunta {answer.question_id}."
                )

            is_correct = chosen_alternative.correcto
            if is_correct:
                correct_answers_count += 1

            diagnostic_result = ResultadoDiagnostico(
                id_usuario=db_user.id_usuario,
                id_pregunta=answer.question_id,
                id_alternativa_elegida=answer.alternative_id,
                es_correcta=is_correct
            )
            results_to_save.append(diagnostic_result)

        # 4. Guardar resultados
        try:
            db.add_all(results_to_save)
            db.commit()
            for result in results_to_save:
                db.refresh(result)
        except Exception as e:
            db.rollback()
            print(f"Error al guardar resultados de diagnóstico: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ocurrió un error al guardar los resultados de la evaluación."
            )

        # 5. Determinar la decisión
        decision = "CONTINUAR" if correct_answers_count == 2 else "FINALIZAR"

        # 6. Retornar la respuesta
        return DiagnosticStage1Response(
            student_id=data.student_id,
            decision=decision,
            correct_answers_count=correct_answers_count,
            message=f"Diagnóstico Etapa 1 completado. Respuestas correctas: {correct_answers_count} de 2."
        )
