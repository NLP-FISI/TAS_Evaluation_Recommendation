# app/core/performance_utils.py
from typing import List, Dict, Any


def _normalize_type(t: Any) -> str | None:
    """
    Normaliza variantes de tipo a: 'literal', 'inferencial', 'critico'
    """
    if t is None:
        return None
    s = str(t).strip().lower()
    if s in ("literal", "lectura", "basico", "básico"):
        return "literal"
    if s in ("inferential", "inferencial", "inferencia", "inferencial"):
        return "inferencial"
    if s in ("critical", "critico", "crítico", "critica"):
        return "critico"
    # si no se reconoce, devolver None para ignorarlo
    return None


def calcular_metricas_por_tipo(answers: List[Dict]) -> Dict[str, float]:
    """
    answers: lista de dicts con claves: 'question_id', 'type', 'is_correct'
      ejemplo: {"question_id": 1, "type": "literal", "is_correct": True}
    Retorna dict: {"literal": 80.0, "inferencial": 60.0, "critico": 50.0}
    """
    tipos = {
        "literal": {"total": 0, "correctas": 0},
        "inferencial": {"total": 0, "correctas": 0},
        "critico": {"total": 0, "correctas": 0},
    }

    for a in answers:
        tip = _normalize_type(a.get("type"))
        if tip is None:
            continue
        tipos[tip]["total"] += 1
        if a.get("is_correct") is True:
            tipos[tip]["correctas"] += 1

    resultados: Dict[str, float] = {}
    for k, v in tipos.items():
        total = v["total"]
        correctas = v["correctas"]
        porcentaje = (correctas / total * 100) if total > 0 else 0.0
        resultados[k] = round(porcentaje, 2)

    return resultados


def calcular_metricas_desde_counts(
    counts: Dict[str, Dict[str, int]]
) -> Dict[str, float]:
    """
    counts: formato esperado, por ejemplo:
    {
      "literal": {"correct": 3, "total": 5},
      "inferencial": {"correct": 2, "total": 4},
      "critico": {"correct": 1, "total": 3}
    }
    Retorna dict de porcentajes como calcular_metricas_por_tipo.
    """
    resultados: Dict[str, float] = {}
    for key in ("literal", "inferencial", "critico"):
        sec = counts.get(key, {})
        correct = sec.get("correct", 0) or sec.get("correctas", 0) or 0
        total = sec.get("total", 0)
        porcentaje = (correct / total * 100) if total > 0 else 0.0
        resultados[key] = round(porcentaje, 2)
    return resultados


def determinar_nivel_global(performance: Dict[str, float]) -> str:
    """
    Determina un nivel global a partir de los porcentajes por tipo.
      - 'Alto': promedio >= 80
      - 'Medio': 50 <= promedio < 80
      - 'Bajo': promedio < 50
    Retorna: "Alto" / "Medio" / "Bajo"
    """
    if not performance:
        return "Bajo"
    promedio = sum(performance.values()) / len(performance)
    if promedio >= 80:
        return "Alto"
    if promedio >= 50:
        return "Medio"
    return "Bajo"


def generar_recomendaciones_detaladas(performance: Dict[str, float]) -> List[str]:
    """
    Genera recomendaciones detalladas y motivadoras (opción B).
    Cada elemento es una recomendación específica para mejorar.
    """
    consejos: List[str] = []

    lit = performance.get("literal", 0.0)
    if lit < 70:
        consejos.append(
            "Tu comprensión literal necesita refuerzo. Te recomendamos practicar con textos "
            "breves (1-2 párrafos) y responder preguntas directas sobre hechos y detalles. "
            "Empieza por identificar nombres, fechas y acciones en cada párrafo y luego resume "
            "en una frase lo que pasó. Haz esto 15 minutos al día durante una semana."
        )
    else:
        consejos.append(
            "Buen nivel en comprensión literal. Mantén la práctica con lecturas variadas y "
            "ejercicios que pidan detalles; intenta resumir cada texto en 2-3 oraciones."
        )

    inf = performance.get("inferencial", 0.0)
    if inf < 70:
        consejos.append(
            "Tu capacidad inferencial puede mejorar. Trabaja con preguntas que pidan inferir causas, "
            "intenciones o consecuencias. Lee un párrafo y pregunta '¿por qué ocurrió esto?' o "
            "'¿qué podría pasar después?'. Discute las respuestas con un compañero o escribe 3 posibles "
            "interpretaciones y justifícalas con evidencia del texto."
        )
    else:
        consejos.append(
            "Buen desempeño inferencial. Desafíate con textos que requieran relacionar ideas y extraer "
            "conclusiones no explícitas; practica justificando tus inferencias con evidencias textuales."
        )

    cri = performance.get("critico", 0.0)
    if cri < 70:
        consejos.append(
            "Para fortalecer el pensamiento crítico, practica analizando argumentos: identifica la tesis, "
            "las evidencias que la sostienen y las posibles falacias. Redacta breves contraargumentos y "
            "valora la solidez de las fuentes. Realiza actividades de comparación entre dos textos sobre "
            "el mismo tema y escribe cuál es más convincente y por qué."
        )
    else:
        consejos.append(
            "Excelente pensamiento crítico. Mantén el nivel enfrentándote a textos controvertidos, "
            "debates y tareas de evaluación de evidencias; intenta liderar un pequeño debate o escribir "
            "una reseña crítica semanal."
        )

    return consejos
