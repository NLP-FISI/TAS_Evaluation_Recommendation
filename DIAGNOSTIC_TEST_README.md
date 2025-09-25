# 🧪 Sistema de Prueba de Diagnóstico - Etapa 1 (Nivel Básico)

## 🎯 Objetivo

Implementar la primera fase de prueba de diagnóstico específicamente diseñada para estudiantes de nivel básico (grados 1-3 de primaria). El sistema evalúa habilidades fundamentales de comprensión lectora, vocabulario y gramática básica.

## ⚙️ Funcionalidades Implementadas

### 📝 Generación de Pruebas Diagnósticas
- ✅ 8 preguntas cuidadosamente diseñadas para nivel básico
- ✅ Cobertura de 3 áreas principales: comprensión lectora, vocabulario y gramática
- ✅ Preguntas contextualizadas con temáticas familiares para niños
- ✅ Instrucciones claras y amigables para estudiantes
- ✅ Límite de tiempo apropiado (20 minutos)

### 📊 Sistema de Evaluación Completo
- ✅ Puntuación general del 0-100%
- ✅ Evaluación específica por área de habilidades
- ✅ Identificación de fortalezas y debilidades
- ✅ Determinación automática del nivel del estudiante
- ✅ Recomendaciones personalizadas basadas en el desempeño
- ✅ Próximos pasos sugeridos para el aprendizaje

## 📡 Endpoints API

### 1. `POST /api/v1/diagnostic-test/generate`
Genera una prueba diagnóstica personalizada.

**Request:**
```json
{
  "student_id": "estudiante123",
  "grade_level": 3,
  "test_level": "básico",
  "preferences": ["animales", "cuentos"]
}
```

**Response:**
```json
{
  "student_id": "estudiante123",
  "test_id": "uuid-generado",
  "questions": [...],
  "instructions": "¡Hola! Vamos a hacer una pequeña prueba...",
  "time_limit": 20
}
```

### 2. `POST /api/v1/diagnostic-test/evaluate`
Evalúa las respuestas del estudiante y genera diagnóstico.

**Request:**
```json
{
  "student_id": "estudiante123",
  "test_id": "uuid-del-test",
  "answers": [
    {
      "question_id": "basic_001",
      "answer": "Miau",
      "time_spent": 30
    }
  ]
}
```

**Response:**
```json
{
  "student_id": "estudiante123",
  "test_id": "uuid-del-test",
  "overall_score": 0.75,
  "overall_level": "básico",
  "skill_assessments": [
    {
      "skill_area": "comprensión_lectora",
      "score": 0.8,
      "level": "intermedio",
      "strengths": ["Excelente comprensión en comprensión_lectora"],
      "weaknesses": []
    }
  ],
  "recommendations": [
    "¡Excelente trabajo! Estás listo para desafíos más avanzados."
  ],
  "next_steps": [
    "Proceder con textos de nivel intermedio"
  ],
  "message": "Diagnóstico completado. Puntuación general: 75.0%"
}
```

### 3. `GET /api/v1/diagnostic-test/questions/basic`
Endpoint de utilidad para obtener las preguntas de nivel básico.

## 📚 Estructura de Preguntas

### Áreas de Evaluación:

1. **Comprensión Lectora (comprensión_lectora)**
   - Preguntas basadas en textos cortos y familiares
   - Evaluación de comprensión literal
   - Identificación de información específica

2. **Vocabulario (vocabulario)**
   - Significado de palabras en contexto
   - Sinónimos y definiciones simples
   - Vocabulario apropiado para la edad

3. **Gramática Básica (gramática)**
   - Identificación de acciones (verbos)
   - Conteo de palabras en oraciones
   - Elementos básicos de estructura oracional

### Tipos de Preguntas:
- **Opción múltiple**: 4 opciones con una respuesta correcta
- **Verdadero/Falso**: Evaluación de comprensión directa

## 🎯 Sistema de Niveles

### Criterios de Evaluación:
- **Puntuación ≥ 80%**: Puede avanzar a nivel intermedio
- **Puntuación 60-79%**: Se mantiene en básico con buen progreso
- **Puntuación < 60%**: Necesita refuerzo en nivel básico

### Recomendaciones Automáticas:
- **Alto rendimiento**: Textos más avanzados y análisis profundo
- **Rendimiento medio**: Refuerzo de áreas débiles y práctica adicional
- **Bajo rendimiento**: Ejercicios fundamentales y vocabulario básico

## 🧪 Testing

El sistema incluye 6 casos de prueba completos:

1. **test_generate_diagnostic_test**: Verifica generación correcta de pruebas
2. **test_evaluate_diagnostic_test**: Prueba evaluación con respuestas mixtas
3. **test_get_basic_level_questions**: Valida endpoint de preguntas
4. **test_diagnostic_test_with_minimal_data**: Prueba con datos mínimos
5. **test_evaluate_diagnostic_with_all_correct_answers**: Caso de rendimiento perfecto
6. **test_evaluate_diagnostic_with_all_wrong_answers**: Caso de bajo rendimiento

Ejecutar tests:
```bash
pytest app/tests/test_diagnostic.py -v
```

## 🔒 Seguridad

- ✅ Análisis CodeQL completado: 0 vulnerabilidades encontradas
- ✅ Validación de entrada con Pydantic
- ✅ Manejo apropiado de errores
- ✅ No exposición de respuestas correctas en endpoints públicos

## 🚀 Próximos Pasos

- [ ] Implementación de Etapa 2 (Nivel Intermedio)
- [ ] Integración con base de datos para persistencia
- [ ] Sistema de reportes para educadores
- [ ] Análisis de tiempo de respuesta por pregunta
- [ ] Adaptación de dificultad basada en desempeño

## 👥 Contribución

Esta implementación sigue las convenciones establecidas en `README_GUIDE.md` y está lista para integrarse con otros módulos del sistema educativo.