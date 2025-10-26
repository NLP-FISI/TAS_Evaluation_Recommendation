# File: app/services/diagnostic_service.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.diagnostic import Pregunta, Alternativa, ResultadoDiagnostico, Texto  # Importamos Texto 
from app.models.usuario import Usuario

# Importar esquemas Pydantic
from app.schemas.diagnostic_schemas import (
    DiagnosticStage1Request,
    DiagnosticStage1Response,
    Answer,
    DiagnosticStage2Request,
    DiagnosticStage2Response,
)

class DiagnosticService:
    """
    Servicio para manejar la lógica del diagnóstico por etapas.
    """

    @staticmethod
    def process_stage1(data: DiagnosticStage1Request, db: Session) -> DiagnosticStage1Response:
        """
        Procesa las respuestas de la Etapa 1 (F-02.A).
        Verifica respuestas, guarda resultados y decide si continuar.
        """
        # 1. Verificar que el usuario exista
        db_user = db.query(Usuario).filter(Usuario.student_id == data.student_id).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con student_id '{data.student_id}' no encontrado."
            )

        correct_count = 0
        now = datetime.utcnow() # Usar UTC para consistencia

        # 2. Procesar cada respuesta
        if len(data.answers) != 2:
             raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Se requieren exactamente 2 respuestas para la Etapa 1."
            )

        processed_questions = set()
        for answer in data.answers:
            if answer.question_id in processed_questions:
                 raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"ID de pregunta duplicado: {answer.question_id}."
                )
            processed_questions.add(answer.question_id)

            # Buscar la alternativa correcta en la BD
            correct_alternative = db.query(Alternativa).filter(
                Alternativa.id_pregunta == answer.question_id,
                Alternativa.correcto == True
            ).first()

            if not correct_alternative:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Pregunta con id '{answer.question_id}' o su alternativa correcta no encontrada."
                )

            # Verificar si la respuesta del usuario es correcta
            is_correct = (answer.alternative_id == correct_alternative.id_alternativa)
            if is_correct:
                correct_count += 1

            # 3. Guardar el resultado en la BD
            db_result = ResultadoDiagnostico(
                id_usuario=db_user.id_usuario,
                id_pregunta=answer.question_id,
                id_alternativa_elegida=answer.alternative_id,
                es_correcta=is_correct,
                fecha_respuesta=now
            )
            db.add(db_result)

        # 4. Aplicar regla de negocio y tomar decisión
        decision = "CONTINUAR" if correct_count == 2 else "FINALIZAR"

        try:
            db.commit() # Guardar todos los resultados
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al guardar resultados en la base de datos: {e}"
            )

        return DiagnosticStage1Response(
            student_id=data.student_id,
            decision=decision,
            correct_answers_count=correct_count,
            message=f"Diagnóstico Etapa 1 completado. Respuestas correctas: {correct_count} de 2."
        )

    @staticmethod
    def process_stage2(data: DiagnosticStage2Request, db: Session) -> DiagnosticStage2Response:
        """
        Procesa las respuestas de la Etapa 2 (F-02.B).
        Verifica respuestas y guarda los resultados detallados.
        La asignación de nivel (Intermedio/Avanzado) se hará en F-03.
        """
        # 1. Verificar que el usuario exista
        db_user = db.query(Usuario).filter(Usuario.student_id == data.student_id).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con student_id '{data.student_id}' no encontrado."
            )

        correct_count = 0
        now = datetime.utcnow()

        # 2. Procesar cada respuesta (ahora esperamos 3)
        if len(data.answers) != 3:
             raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Se requieren exactamente 3 respuestas para la Etapa 2."
            )

        processed_questions = set()
        for answer in data.answers:
            if answer.question_id in processed_questions:
                 raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"ID de pregunta duplicado: {answer.question_id}."
                )
            processed_questions.add(answer.question_id)

            # Buscar la alternativa correcta en la BD
            correct_alternative = db.query(Alternativa).filter(
                Alternativa.id_pregunta == answer.question_id,
                Alternativa.correcto == True
            ).first()

            if not correct_alternative:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Pregunta con id '{answer.question_id}' o su alternativa correcta no encontrada."
                )

            # Verificar si la respuesta del usuario es correcta
            is_correct = (answer.alternative_id == correct_alternative.id_alternativa)
            if is_correct:
                correct_count += 1

            # 3. Guardar el resultado en la BD
            db_result = ResultadoDiagnostico(
                id_usuario=db_user.id_usuario,
                id_pregunta=answer.question_id,
                id_alternativa_elegida=answer.alternative_id,
                es_correcta=is_correct,
                fecha_respuesta=now
            )
            db.add(db_result)

        try:
            db.commit() # Guardar todos los resultados
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al guardar resultados de Etapa 2 en la base de datos: {e}"
            )

        return DiagnosticStage2Response(
            student_id=data.student_id,
            correct_answers_count=correct_count,
            message=f"Diagnóstico Etapa 2 completado. Respuestas correctas: {correct_count} de 3."
        )

