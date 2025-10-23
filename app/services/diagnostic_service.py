"""
Servicio para manejar la lógica de negocio del diagnóstico inicial (Etapa 1).
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.schemas.diagnostic_schemas import DiagnosticStage1Request, DiagnosticStage1Response, Answer
from app.models.diagnostic import Pregunta, Alternativa, ResultadoDiagnostico, Texto # Importamos Texto también
from app.models.user_profile import Usuario # Asumimos que Usuario está en user_profile

class DiagnosticService:

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

        # 2. Verificar que se enviaron exactamente 2 respuestas
        if len(data.answers) != 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Se deben enviar exactamente 2 respuestas para la Etapa 1."
            )

        correct_answers_count = 0
        results_to_save = []

        # 3. Procesar cada respuesta
        for answer in data.answers:
            # Buscar la alternativa elegida por el usuario
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

            # Crear registro para guardar en la BD
            diagnostic_result = ResultadoDiagnostico(
                id_usuario=db_user.id_usuario,
                id_pregunta=answer.question_id,
                id_alternativa_elegida=answer.alternative_id,
                es_correcta=is_correct
            )
            results_to_save.append(diagnostic_result)

        # 4. Guardar todos los resultados en la BD
        try:
            db.add_all(results_to_save)
            db.commit()
            for result in results_to_save:
                db.refresh(result) # Actualiza los objetos con IDs, etc.
        except Exception as e:
            db.rollback()
            print(f"Error al guardar resultados de diagnóstico: {e}") # Log del error
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ocurrió un error al guardar los resultados de la evaluación."
            )

        # 5. Determinar la decisión (Continuar o Finalizar)
        decision = "CONTINUAR" if correct_answers_count == 2 else "FINALIZAR"

        # 6. Devolver la respuesta
        return DiagnosticStage1Response(
            student_id=data.student_id,
            decision=decision,
            correct_answers_count=correct_answers_count,
            message=f"Diagnóstico Etapa 1 completado. Respuestas correctas: {correct_answers_count} de 2."
        )

