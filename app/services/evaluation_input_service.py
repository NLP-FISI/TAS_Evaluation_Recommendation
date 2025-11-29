# File: app/services/evaluation_input_service.py
from typing import List
import re
from sqlalchemy.orm import Session
from app.schemas.evaluation_schemas import (
    EvaluationInputRequest, 
    EvaluationInputResponse,
    TextWithQuestions,
    QuestionInfo,
    AlternativeInfo
)
from app.models.pregunta import Pregunta


class EvaluationInputService:
    @staticmethod
    def _strip_html_tags(html_content: str) -> str:
        """
        Elimina todas las etiquetas HTML y retorna solo el texto plano.
        """
        # Eliminar etiquetas <style>...</style>
        clean = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL)
        # Eliminar etiquetas <script>...</script>
        clean = re.sub(r'<script[^>]*>.*?</script>', '', clean, flags=re.DOTALL)
        # Eliminar todas las demás etiquetas HTML
        clean = re.sub(r'<[^>]+>', '', clean)
        # Limpiar espacios múltiples y saltos de línea
        clean = re.sub(r'\n\s*\n', '\n\n', clean)
        clean = re.sub(r' +', ' ', clean)
        return clean.strip()
    
    @staticmethod
    def evaluate_student(data: EvaluationInputRequest, db: Session) -> EvaluationInputResponse:
        """
        Lógica de negocio para evaluar al estudiante al inicio.
        Devuelve los dos primeros textos (ID 1 y 2) con sus preguntas.
        """

        # Determinar nivel inicial basado en grado
        if data.grade_level <= 3:
            level = "básico"
        else:
            level = "intermedio"

        # Obtener textos con ID 1 y 2 (los dos primeros textos de diagnóstico)
        texto_ids = [1, 2]
        
        # Consultar preguntas asociadas a estos textos
        preguntas = (
            db.query(Pregunta)
            .filter(Pregunta.id_texto.in_(texto_ids))
            .order_by(Pregunta.id_texto, Pregunta.id_pregunta)
            .all()
        )
        
        # Agrupar preguntas por texto
        textos_dict = {}
        for pregunta in preguntas:
            texto = pregunta.texto
            if not texto:
                continue
                
            if texto.id_texto not in textos_dict:
                # Detectar formato
                has_html = bool(texto.contenido and ('<' in texto.contenido and '>' in texto.contenido))
                
                # Para evaluation-input, siempre devolver texto plano (sin HTML)
                content = texto.contenido or ""
                if has_html:
                    content = EvaluationInputService._strip_html_tags(content)
                
                textos_dict[texto.id_texto] = {
                    'text_id': texto.id_texto,
                    'title': texto.titulo or f"Texto {texto.id_texto}",
                    'content': content,
                    'format': 'plain',  # Siempre plain para este endpoint
                    'questions': []
                }
            
            # Construir alternativas
            alternatives = [
                AlternativeInfo(
                    alternative_id=alt.id_alternativa,
                    text=alt.contenido
                )
                for alt in pregunta.alternativas
            ]
            
            # Agregar pregunta
            textos_dict[texto.id_texto]['questions'].append(
                QuestionInfo(
                    question_id=pregunta.id_pregunta,
                    question_text=pregunta.contenido,
                    alternatives=alternatives
                )
            )
        
        # Convertir dict a lista de TextWithQuestions
        texts = [
            TextWithQuestions(**text_data)
            for text_data in textos_dict.values()
        ]

        return EvaluationInputResponse(
            student_id=data.student_id,
            initial_level=level,
            texts=texts,
            message=f"Evaluación inicial completada. Se proporcionan {len(texts)} textos de diagnóstico."
        )
