# This module handles the business logic for diagnostic testing - Stage 1: Basic Level
from typing import List, Dict
import uuid
from app.schemas.diagnostic_schemas import (
    DiagnosticTestRequest, DiagnosticTestResponse, DiagnosticTestSubmission,
    DiagnosticResultsResponse, DiagnosticQuestion, StudentAnswer, SkillAssessment,
    DifficultLevel, QuestionType
)


class DiagnosticTestService:
    @staticmethod
    def _get_basic_level_questions() -> List[DiagnosticQuestion]:
        """
        Genera preguntas de diagnóstico para el nivel básico (Etapa 1).
        Estas preguntas evalúan habilidades fundamentales de comprensión lectora.
        """
        return [
            DiagnosticQuestion(
                question_id="basic_001",
                question_text="Lee el siguiente texto:\n\n'El gato de María se llama Miau. Miau es muy juguetón y le gusta perseguir pelotas. Todos los días, María juega con Miau en el jardín.'\n\n¿Cómo se llama el gato de María?",
                question_type=QuestionType.MULTIPLE_CHOICE,
                options=["Pelota", "Miau", "María", "Jardín"],
                correct_answer="Miau",
                skill_area="comprensión_lectora",
                difficulty_level=DifficultLevel.BASIC
            ),
            DiagnosticQuestion(
                question_id="basic_002",
                question_text="En el texto anterior, ¿dónde juega María con su gato?",
                question_type=QuestionType.MULTIPLE_CHOICE,
                options=["En la casa", "En el jardín", "En la escuela", "En el parque"],
                correct_answer="En el jardín",
                skill_area="comprensión_lectora",
                difficulty_level=DifficultLevel.BASIC
            ),
            DiagnosticQuestion(
                question_id="basic_003",
                question_text="¿El gato Miau es juguetón?",
                question_type=QuestionType.TRUE_FALSE,
                options=["Verdadero", "Falso"],
                correct_answer="Verdadero",
                skill_area="comprensión_lectora",
                difficulty_level=DifficultLevel.BASIC
            ),
            DiagnosticQuestion(
                question_id="basic_004",
                question_text="¿Cuál de estas palabras significa lo mismo que 'juguetón'?",
                question_type=QuestionType.MULTIPLE_CHOICE,
                options=["Triste", "Divertido", "Cansado", "Enojado"],
                correct_answer="Divertido",
                skill_area="vocabulario",
                difficulty_level=DifficultLevel.BASIC
            ),
            DiagnosticQuestion(
                question_id="basic_005",
                question_text="Lee esta oración: 'Los niños corren en el patio.' ¿Cuál es la acción que hacen los niños?",
                question_type=QuestionType.MULTIPLE_CHOICE,
                options=["Caminar", "Correr", "Saltar", "Jugar"],
                correct_answer="Correr",
                skill_area="gramática",
                difficulty_level=DifficultLevel.BASIC
            ),
            DiagnosticQuestion(
                question_id="basic_006",
                question_text="¿Cuántas palabras hay en esta oración? 'El perro ladra fuerte.'",
                question_type=QuestionType.MULTIPLE_CHOICE,
                options=["3", "4", "5", "6"],
                correct_answer="4",
                skill_area="gramática",
                difficulty_level=DifficultLevel.BASIC
            ),
            DiagnosticQuestion(
                question_id="basic_007",
                question_text="Lee: 'Ana tiene una manzana roja. La manzana está muy dulce.' ¿De qué color es la manzana de Ana?",
                question_type=QuestionType.MULTIPLE_CHOICE,
                options=["Verde", "Amarilla", "Roja", "Azul"],
                correct_answer="Roja",
                skill_area="comprensión_lectora",
                difficulty_level=DifficultLevel.BASIC
            ),
            DiagnosticQuestion(
                question_id="basic_008",
                question_text="¿Qué significa la palabra 'dulce' en el texto anterior?",
                question_type=QuestionType.MULTIPLE_CHOICE,
                options=["Que sabe rico", "Que es grande", "Que es pequeña", "Que es cara"],
                correct_answer="Que sabe rico",
                skill_area="vocabulario",
                difficulty_level=DifficultLevel.BASIC
            )
        ]

    @staticmethod
    def generate_diagnostic_test(data: DiagnosticTestRequest) -> DiagnosticTestResponse:
        """
        Genera una prueba de diagnóstico para un estudiante específico.
        Para la Etapa 1, siempre se genera un test de nivel básico.
        """
        test_id = str(uuid.uuid4())
        
        # Para la Etapa 1, siempre usamos preguntas de nivel básico
        questions = DiagnosticTestService._get_basic_level_questions()
        
        # Instrucciones específicas para el nivel básico
        instructions = """
        ¡Hola! Vamos a hacer una pequeña prueba para conocerte mejor.
        
        Instrucciones:
        - Lee cada pregunta con cuidado
        - Elige la respuesta que crees que es correcta
        - No te preocupes si no sabes alguna respuesta
        - Tómate tu tiempo
        
        ¡Empecemos!
        """
        
        return DiagnosticTestResponse(
            student_id=data.student_id,
            test_id=test_id,
            questions=questions,
            instructions=instructions.strip(),
            time_limit=20  # 20 minutos para el test básico
        )

    @staticmethod
    def evaluate_diagnostic_test(submission: DiagnosticTestSubmission) -> DiagnosticResultsResponse:
        """
        Evalúa las respuestas del estudiante y genera un diagnóstico completo.
        """
        # Obtener las preguntas correctas para comparar
        correct_questions = {q.question_id: q for q in DiagnosticTestService._get_basic_level_questions()}
        
        # Evaluar cada respuesta
        skill_scores = {}
        total_questions = 0
        correct_answers = 0
        
        for answer in submission.answers:
            if answer.question_id in correct_questions:
                question = correct_questions[answer.question_id]
                skill_area = question.skill_area
                
                if skill_area not in skill_scores:
                    skill_scores[skill_area] = {"correct": 0, "total": 0}
                
                skill_scores[skill_area]["total"] += 1
                total_questions += 1
                
                if answer.answer == question.correct_answer:
                    skill_scores[skill_area]["correct"] += 1
                    correct_answers += 1
        
        # Calcular puntuación general
        overall_score = correct_answers / total_questions if total_questions > 0 else 0
        
        # Determinar nivel general
        if overall_score >= 0.8:
            overall_level = DifficultLevel.INTERMEDIATE  # Puede avanzar al siguiente nivel
        elif overall_score >= 0.6:
            overall_level = DifficultLevel.BASIC  # Se mantiene en básico pero con buen progreso
        else:
            overall_level = DifficultLevel.BASIC  # Necesita refuerzo en nivel básico
        
        # Evaluar habilidades específicas
        skill_assessments = []
        for skill_area, scores in skill_scores.items():
            skill_score = scores["correct"] / scores["total"] if scores["total"] > 0 else 0
            
            # Determinar fortalezas y debilidades
            strengths = []
            weaknesses = []
            
            if skill_score >= 0.8:
                strengths.append(f"Excelente comprensión en {skill_area}")
            elif skill_score >= 0.6:
                strengths.append(f"Buen desempeño en {skill_area}")
            else:
                weaknesses.append(f"Necesita práctica en {skill_area}")
            
            skill_level = DifficultLevel.BASIC
            if skill_score >= 0.8:
                skill_level = DifficultLevel.INTERMEDIATE
            
            skill_assessments.append(SkillAssessment(
                skill_area=skill_area,
                score=skill_score,
                level=skill_level,
                strengths=strengths,
                weaknesses=weaknesses
            ))
        
        # Generar recomendaciones basadas en el desempeño
        recommendations = []
        next_steps = []
        
        if overall_score >= 0.8:
            recommendations.append("¡Excelente trabajo! Estás listo para desafíos más avanzados.")
            next_steps.append("Proceder con textos de nivel intermedio")
            next_steps.append("Introducir preguntas de análisis más profundo")
        elif overall_score >= 0.6:
            recommendations.append("Buen progreso. Continúa practicando para fortalecer tus habilidades.")
            next_steps.append("Reforzar áreas débiles con ejercicios adicionales")
            next_steps.append("Practicar más lecturas de nivel básico")
        else:
            recommendations.append("Necesitas más práctica en habilidades fundamentales.")
            next_steps.append("Enfocarse en ejercicios de comprensión básica")
            next_steps.append("Trabajar vocabulario fundamental")
            next_steps.append("Practicar lectura de textos simples")
        
        # Recomendaciones específicas por habilidad
        for assessment in skill_assessments:
            if assessment.score < 0.6:
                if assessment.skill_area == "comprensión_lectora":
                    recommendations.append("Practica leyendo textos cortos y respondiendo preguntas simples.")
                elif assessment.skill_area == "vocabulario":
                    recommendations.append("Aprende nuevas palabras cada día y úsalas en oraciones.")
                elif assessment.skill_area == "gramática":
                    recommendations.append("Practica identificando partes de oraciones simples.")
        
        message = f"Diagnóstico completado. Puntuación general: {overall_score:.1%}"
        
        return DiagnosticResultsResponse(
            student_id=submission.student_id,
            test_id=submission.test_id,
            overall_score=overall_score,
            overall_level=overall_level,
            skill_assessments=skill_assessments,
            recommendations=recommendations,
            next_steps=next_steps,
            message=message
        )