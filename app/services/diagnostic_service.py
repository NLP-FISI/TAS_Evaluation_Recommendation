# File: app/services/diagnostic_service.py
from datetime import datetime
from typing import List, Set

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

# Modelos
from app.models.usuario import Usuario
from app.models.diagnostic import Alternativa, ResultadoDiagnostico
from app.models.desempenio import Desempenio
from app.models.grado import Grado

# Esquemas
from app.schemas.diagnostic_schemas import (
    DiagnosticStage1Request, DiagnosticStage1Response, Answer,
    DiagnosticStage2Request, DiagnosticStage2Response,
    LevelAssignmentRequest, LevelAssignmentResponse
)

# IDs fijos de preguntas por etapa (ajusta si cambian en tu BD)
STAGE_1_QUESTIONS: List[int] = [1, 2]
STAGE_2_QUESTIONS: List[int] = [3, 4, 5]


class DiagnosticService:
    """
    Servicio para manejar la lógica del diagnóstico por etapas (F-02 y F-03).
    """

    # ------------ Helpers ------------

    @staticmethod
    def _get_user_by_student_id(db: Session, student_id: str) -> Usuario:
        user = db.query(Usuario).filter(Usuario.student_id == student_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con student_id '{student_id}' no encontrado."
            )
        return user

    @staticmethod
    def _validate_answers_stage(answers: List[Answer], expected_qids: List[int]) -> None:
        """
        Verifica:
        - Cantidad exacta de respuestas
        - No hay preguntas duplicadas
        - Las preguntas pertenecen al set permitido para la etapa
        """
        if len(answers) != len(expected_qids):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Se requieren exactamente {len(expected_qids)} respuestas para esta etapa."
            )

        seen: Set[int] = set()
        allowed: Set[int] = set(expected_qids)
        for a in answers:
            if a.question_id in seen:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"ID de pregunta duplicado: {a.question_id}."
                )
            seen.add(a.question_id)

            if a.question_id not in allowed:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"La pregunta {a.question_id} no pertenece a esta etapa."
                )

    @staticmethod
    def _save_diagnostic_results(db: Session, user_id: int, answers: List[Answer]) -> int:
        """
        Procesa y guarda resultados:
        - La corrección se infiere de la alternativa elegida (flag Alternativa.correcto)
        - Valida que la alternativa corresponda a la pregunta indicada
        """
        now = datetime.utcnow()
        to_save: List[ResultadoDiagnostico] = []
        correct_count = 0

        for ans in answers:
            chosen = db.query(Alternativa).filter(
                Alternativa.id_alternativa == ans.alternative_id,
                Alternativa.id_pregunta == ans.question_id
            ).first()

            if not chosen:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Alternativa {ans.alternative_id} no encontrada para Pregunta {ans.question_id}."
                )

            is_correct = bool(chosen.correcto)
            if is_correct:
                correct_count += 1

            to_save.append(
                ResultadoDiagnostico(
                    id_usuario=user_id,
                    id_pregunta=ans.question_id,
                    id_alternativa_elegida=ans.alternative_id,
                    es_correcta=is_correct,
                    fecha_respuesta=now
                )
            )

        db.add_all(to_save)
        return correct_count

    # ------------ F-02.A ------------

    @staticmethod
    def process_stage1(data: DiagnosticStage1Request, db: Session) -> DiagnosticStage1Response:
        user = DiagnosticService._get_user_by_student_id(db, data.student_id)
        DiagnosticService._validate_answers_stage(data.answers, STAGE_1_QUESTIONS)

        try:
            correct = DiagnosticService._save_diagnostic_results(db, user.id_usuario, data.answers)
            decision = "CONTINUAR" if correct == len(STAGE_1_QUESTIONS) else "FINALIZAR"
            db.commit()
        except HTTPException:
            db.rollback()
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error en Etapa 1: {e}"
            )

        return DiagnosticStage1Response(
            student_id=data.student_id,
            decision=decision,
            correct_answers_count=correct,
            message=f"Diagnóstico Etapa 1 completado. Respuestas correctas: {correct} de {len(STAGE_1_QUESTIONS)}."
        )

    # ------------ F-02.B ------------

    @staticmethod
    def process_stage2(data: DiagnosticStage2Request, db: Session) -> DiagnosticStage2Response:
        user = DiagnosticService._get_user_by_student_id(db, data.student_id)
        DiagnosticService._validate_answers_stage(data.answers, STAGE_2_QUESTIONS)

        try:
            correct = DiagnosticService._save_diagnostic_results(db, user.id_usuario, data.answers)
            db.commit()
        except HTTPException:
            db.rollback()
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error en Etapa 2: {e}"
            )

        return DiagnosticStage2Response(
            student_id=data.student_id,
            correct_answers_count=correct,
            message=f"Diagnóstico Etapa 2 completado. Respuestas correctas: {correct} de {len(STAGE_2_QUESTIONS)}."
        )

    # ------------ F-03 (Asignación de nivel inicial, sin ELO) ------------

    @staticmethod
    def assign_initial_level(data: LevelAssignmentRequest, db: Session) -> LevelAssignmentResponse:
        user = DiagnosticService._get_user_by_student_id(db, data.student_id)

        # ESTRATEGIA: Buscar primero solo Stage 1, luego Stage 2 si es necesario
        # Esto evita problemas de mezclar timestamps de diferentes etapas
        
        # PASO 1: Buscar las 2 respuestas MÁS RECIENTES de STAGE 1
        stage1_results = db.query(ResultadoDiagnostico)\
            .filter(
                ResultadoDiagnostico.id_usuario == user.id_usuario,
                ResultadoDiagnostico.id_pregunta.in_(STAGE_1_QUESTIONS)
            )\
            .order_by(ResultadoDiagnostico.fecha_respuesta.desc())\
            .limit(2)\
            .all()

        if len(stage1_results) < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No se encontraron suficientes resultados de Stage 1 para el usuario {data.student_id}. Se necesitan 2 respuestas."
            )

        # Verificar que las 2 respuestas sean del mismo intento (máximo 5 segundos de diferencia)
        from datetime import timedelta
        time_diff = abs((stage1_results[0].fecha_respuesta - stage1_results[1].fecha_respuesta).total_seconds())
        
        if time_diff > 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Las respuestas de Stage 1 parecen ser de intentos diferentes (diferencia: {time_diff:.1f}s). "
                       f"Por favor, completa un nuevo diagnóstico."
            )

        print(f"\n{'='*70}")
        print(f"DEBUG - Usuario {data.student_id} (id={user.id_usuario})")
        print(f"\nDEBUG - STAGE 1 (Preguntas {STAGE_1_QUESTIONS}):")
        for r in stage1_results:
            print(f"  Pregunta {r.id_pregunta}: es_correcta={r.es_correcta}, fecha={r.fecha_respuesta}")
        
        stage1_correct = sum(1 for r in stage1_results if r.es_correcta)
        print(f"\n  ✅ Total aciertos Stage 1: {stage1_correct}/2")

        # DECISIÓN BASADA EN STAGE 1
        if stage1_correct == 0:
            nivel = "2do Grado"
            print(f"  📊 Resultado: 0 aciertos → {nivel} (FIN)")
            print(f"{'='*70}\n")
        elif stage1_correct == 1:
            nivel = "3er Grado"
            print(f"  📊 Resultado: 1 acierto → {nivel} (FIN)")
            print(f"{'='*70}\n")
        else:  # stage1_correct == 2
            print(f"  ⏭️  Resultado: 2 aciertos → Continuar a STAGE 2\n")
            
            # PASO 2: Buscar las 3 respuestas MÁS RECIENTES de STAGE 2
            stage2_results = db.query(ResultadoDiagnostico)\
                .filter(
                    ResultadoDiagnostico.id_usuario == user.id_usuario,
                    ResultadoDiagnostico.id_pregunta.in_(STAGE_2_QUESTIONS)
                )\
                .order_by(ResultadoDiagnostico.fecha_respuesta.desc())\
                .limit(3)\
                .all()

            if len(stage2_results) < 3:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El usuario {data.student_id} pasó Stage 1 pero no completó Stage 2. Se necesitan 3 respuestas de Stage 2."
                )
            
            # Verificar que las 3 respuestas sean del mismo intento (máximo 5 segundos entre la primera y última)
            from datetime import timedelta
            time_span = abs((stage2_results[0].fecha_respuesta - stage2_results[-1].fecha_respuesta).total_seconds())
            
            if time_span > 5:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Las respuestas de Stage 2 parecen ser de intentos diferentes (diferencia: {time_span:.1f}s). "
                           f"Por favor, completa un nuevo diagnóstico."
                )

            print(f"DEBUG - STAGE 2 (Preguntas {STAGE_2_QUESTIONS}):")
            for r in stage2_results:
                print(f"  Pregunta {r.id_pregunta}: es_correcta={r.es_correcta}, fecha={r.fecha_respuesta}")
            
            stage2_correct = sum(1 for r in stage2_results if r.es_correcta)
            print(f"\n  ✅ Total aciertos Stage 2: {stage2_correct}/3")
            
            # Asignar nivel según aciertos en Stage 2
            if stage2_correct == 0:
                nivel = "3er Grado"
            elif stage2_correct == 1:
                nivel = "4to Grado"
            elif stage2_correct == 2:
                nivel = "5to Grado"
            else:  # stage2_correct == 3
                nivel = "6to Grado"
            
            print(f"  📊 Resultado: {stage2_correct} aciertos → {nivel}")
            print(f"{'='*70}\n")

        # Obtener el ID del grado desde la tabla grado
        # La lógica de mapeo es:
        # "2do Grado" -> id_grado = 2
        # "3er Grado" -> id_grado = 3
        # "4to Grado" -> id_grado = 4
        # "5to Grado" -> id_grado = 5
        # "6to Grado" -> id_grado = 6
        
        # Extraer el número del nivel (ej: "3er Grado" -> 3)
        import re
        match = re.search(r'(\d+)', nivel)
        if not match:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"No se pudo extraer el número de grado de '{nivel}'"
            )
        
        grado_numero = int(match.group(1))
        print(f"\nDEBUG - Buscando grado con id_grado: {grado_numero}")
        
        grado = db.query(Grado).filter(Grado.id_grado == grado_numero).first()
        
        if not grado:
            # Mostrar todos los grados disponibles para debug
            all_grados = db.query(Grado).all()
            available = [(g.id_grado, g.nombre_grado) for g in all_grados]
            print(f"DEBUG - Grados disponibles en BD: {available}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"No se encontró el grado con id {grado_numero} en la base de datos. Disponibles: {available}"
            )
        
        print(f"DEBUG - Grado encontrado: id={grado.id_grado}, nombre='{grado.nombre_grado}'")

        # Upsert en Desempenio
        try:
            perf = db.query(Desempenio).filter(Desempenio.id_usuario == user.id_usuario).first()
            if perf:
                perf.nivel = nivel
                perf.nivel_grado_id = grado.id_grado
            else:
                # Crear nuevo registro con valores por defecto para campos NOT NULL
                perf = Desempenio(
                    id_usuario=user.id_usuario,
                    nivel=nivel,
                    nivel_grado_id=grado.id_grado,
                    puntaje=0.0,  # Valor por defecto
                    exactitud=0.0,  # Valor por defecto
                    promedio_tiempo_por_pregunta=0.0,  # Valor por defecto
                    promedio_tiempo_por_lectura=0.0,  # Valor por defecto
                    textos_considerados=0  # Valor por defecto
                )
                db.add(perf)

            db.commit()
            db.refresh(perf)
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al guardar el nivel: {e}"
            )

        return LevelAssignmentResponse(
            student_id=data.student_id,
            assigned_level_label=nivel,
            assigned_level_grade=grado.id_grado,
            message="Nivel de competencia inicial asignado exitosamente."
        )
