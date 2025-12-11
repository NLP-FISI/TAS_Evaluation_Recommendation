# 🎯 Beneficios Clave de los Módulos de Perfilamiento y Diagnóstico

## 📋 Tabla de Contenidos
- [Módulo de Perfilamiento](#módulo-de-perfilamiento)
- [Módulo de Diagnóstico](#módulo-de-diagnóstico)
- [Flujo Completo](#flujo-completo-para-el-frontend)
- [Ventajas para el Frontend Web](#ventajas-para-el-frontend-web)

---

## 🔷 Módulo de Perfilamiento

**Archivo:** `app/services/profiling_service.py`

### **Beneficios Clave**
- ✅ **Personalización desde el inicio**: Crea el perfil del estudiante antes de comenzar
- ✅ **Flexibilidad**: Permite actualizar perfiles existentes sin perder datos
- ✅ **Validación robusta**: Verifica que grados y temáticas existan en la BD
- ✅ **Gestión automática**: Crea grados faltantes automáticamente

### **Qué Contiene**
- Registro/actualización de estudiantes con `student_id` único
- Asignación de grado escolar (1-6)
- Selección de preferencias temáticas (múltiples)
- Creación de usuarios con datos mínimos requeridos

### **Endpoint API**

**Request:**
```http
POST /api/v1/profiling
Content-Type: application/json

{
  "student_id": "EST12345",
  "grade_level": 3,
  "preferences": [1, 3, 5]
}
```

**Response:**
```json
{
  "student_id": "EST12345",
  "profile_created": true,
  "message": "Perfil de usuario creado exitosamente."
}
```

### **Ejemplo de Integración Frontend**

```javascript
// Vue 3 / React
const createProfile = async (studentData) => {
  try {
    const response = await axios.post('/api/v1/profiling', {
      student_id: studentData.id,
      grade_level: studentData.grade,
      preferences: studentData.selectedTopics // [1, 3, 5]
    });
    
    if (response.data.profile_created) {
      console.log('✅ Perfil creado:', response.data.message);
      // Redirigir a diagnóstico
      router.push('/diagnostic/stage1');
    }
  } catch (error) {
    console.error('❌ Error:', error.response.data.detail);
  }
};
```

---

## 🔶 Módulo de Diagnóstico

**Archivo:** `app/services/diagnostic_service.py`

### **Beneficios Clave**
- ✅ **Evaluación adaptativa por etapas**: 2 etapas con lógica condicional
- ✅ **Decisión inteligente**: Si falla Etapa 1 → no continúa a Etapa 2
- ✅ **Historial completo**: Guarda todas las respuestas en BD
- ✅ **Asignación automática de nivel**: Calcula nivel inicial del estudiante
- ✅ **Textos enriquecidos**: Soporta HTML con imágenes (Etapa 2)
- ✅ **Validación estricta**: Sin duplicados, preguntas correctas por etapa

### **Qué Contiene**

#### **Etapa 1**
- 2 preguntas (IDs: 1, 2)
- Texto plano: "La mentira del erizo"
- Texto ID: 1
- Decisión: CONTINUAR (2/2 correctas) o FINALIZAR (< 2 correctas)

#### **Etapa 2**
- 3 preguntas (IDs: 3, 4, 5)
- Texto HTML con imágenes: "Tráfico animal"
- Texto ID: 2
- Solo accesible si pasó Etapa 1

#### **Asignación de Nivel**
- **Básico**: Stage 1 incompleto o Stage 2 con 0-1 correctas
- **Intermedio**: Stage 2 con 2 correctas
- **Avanzado**: Stage 2 con 3 correctas

---

## 🔀 APIs del Diagnóstico

### **1. Obtener Textos por Etapa**

**Request:**
```http
GET /api/v1/diagnostic/texts?stage=1
```

**Response Etapa 1 (Texto Plano):**
```json
{
  "stage": 1,
  "texts": [
    {
      "text_id": 1,
      "title": "La mentira del erizo",
      "content": "Hace mucho tiempo, en un bosque lejano, todos los animales decidieron elegir a su rey...",
      "format": "plain",
      "questions": [
        {
          "question_id": 1,
          "question_text": "¿Qué hizo el erizo para verse mejor?",
          "alternatives": [
            {
              "alternative_id": 1,
              "text": "Se lavó bien las púas."
            },
            {
              "alternative_id": 2,
              "text": "Se peinó con mucho cuidado."
            },
            {
              "alternative_id": 3,
              "text": "Se cubrió el lomo con rosas."
            }
          ]
        },
        {
          "question_id": 2,
          "question_text": "¿Por qué los animales se preocuparon por verse mejor?",
          "alternatives": [
            {
              "alternative_id": 4,
              "text": "Porque eran muy vanidosos con su pelaje."
            },
            {
              "alternative_id": 5,
              "text": "Porque querían convertirse en el nuevo rey."
            },
            {
              "alternative_id": 6,
              "text": "Porque estaban aburridos de su aspecto."
            }
          ]
        }
      ]
    }
  ],
  "message": "Textos de diagnóstico para la etapa 1 obtenidos exitosamente."
}
```

**Response Etapa 2 (Texto HTML):**
```json
{
  "stage": 2,
  "texts": [
    {
      "text_id": 2,
      "title": "Tráfico animal",
      "content": "<div class=\"afiche-animales\"><h1>¡Miles de animales NUNCA más regresarán a su hogar!</h1>...</div><style>...</style>",
      "format": "html",
      "questions": [
        {
          "question_id": 3,
          "question_text": "Según el texto, ¿cuántos animales vivos fueron rescatados solo en el año 2017?",
          "alternatives": [...]
        }
      ]
    }
  ],
  "message": "Textos de diagnóstico para la etapa 2 obtenidos exitosamente."
}
```

---

### **2. Enviar Respuestas Etapa 1**

**Request:**
```http
POST /api/v1/diagnostic/stage1
Content-Type: application/json

{
  "student_id": "EST12345",
  "answers": [
    {
      "question_id": 1,
      "alternative_id": 3
    },
    {
      "question_id": 2,
      "alternative_id": 5
    }
  ]
}
```

**Response:**
```json
{
  "student_id": "EST12345",
  "decision": "CONTINUAR",
  "correct_count": 2,
  "message": "Diagnóstico Etapa 1 completado. Respuestas correctas: 2 de 2."
}
```

**Posibles valores de `decision`:**
- `"CONTINUAR"`: Todas las respuestas correctas → Pasar a Etapa 2
- `"FINALIZAR"`: Algunas incorrectas → Terminar diagnóstico, nivel básico

---

### **3. Enviar Respuestas Etapa 2**

**Request:**
```http
POST /api/v1/diagnostic/stage2
Content-Type: application/json

{
  "student_id": "EST12345",
  "answers": [
    {
      "question_id": 3,
      "alternative_id": 9
    },
    {
      "question_id": 4,
      "alternative_id": 12
    },
    {
      "question_id": 5,
      "alternative_id": 17
    }
  ]
}
```

**Response:**
```json
{
  "student_id": "EST12345",
  "correct_count": 2,
  "message": "Diagnóstico Etapa 2 completado. Respuestas correctas: 2 de 3."
}
```

---

### **4. Asignar Nivel Final**

**Request:**
```http
POST /api/v1/diagnostic/assign-level
Content-Type: application/json

{
  "student_id": "EST12345"
}
```

**Response:**
```json
{
  "student_id": "EST12345",
  "assigned_level": "Intermedio",
  "stage1_correct": 2,
  "stage2_correct": 2,
  "message": "Nivel 'Intermedio' asignado exitosamente basado en el diagnóstico."
}
```

**Lógica de asignación:**
- **Básico**: Stage 1 incompleto (< 2 correctas) o Stage 2 con 0-1 correctas
- **Intermedio**: Stage 2 con 2 correctas
- **Avanzado**: Stage 2 con 3 correctas

---

## 🎨 Flujo Completo para el Frontend

```
┌─────────────────────────────────────────────────────────────┐
│ 1. PERFILAMIENTO                                            │
│    POST /api/v1/profiling                                   │
│    ↓                                                         │
│    Crear perfil estudiante (grado + preferencias)           │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. DIAGNÓSTICO ETAPA 1                                      │
│    GET /api/v1/diagnostic/texts?stage=1                     │
│    ↓                                                         │
│    Mostrar texto "La mentira del erizo" + 2 preguntas       │
│    ↓                                                         │
│    POST /api/v1/diagnostic/stage1                           │
│    ↓                                                         │
│    Decisión: "CONTINUAR" o "FINALIZAR"                      │
└─────────────────────────────────────────────────────────────┘
                            ↓
                   ┌────────┴────────┐
                   │                 │
            CONTINUAR          FINALIZAR
                   │                 │
                   ↓                 ↓
┌──────────────────────────┐  ┌──────────────────────┐
│ 3. DIAGNÓSTICO ETAPA 2   │  │ Nivel Básico         │
│    GET /texts?stage=2    │  │ (saltarse Etapa 2)   │
│    ↓                     │  └──────────────────────┘
│    Texto HTML + 3 preg.  │
│    ↓                     │
│    POST /stage2          │
└──────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. ASIGNACIÓN DE NIVEL                                      │
│    POST /api/v1/diagnostic/assign-level                     │
│    ↓                                                         │
│    Calcular nivel final (Básico/Intermedio/Avanzado)        │
│    ↓                                                         │
│    Guardar en Usuario.id_desempenio                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Ventajas para el Frontend Web

| Aspecto | Beneficio | Implementación |
|---------|-----------|----------------|
| **UX Progresiva** | Diagnóstico en 2 pasos, no abruma al estudiante | Renderizar componentes por etapa |
| **Contenido Rico** | Soporta HTML + imágenes en Etapa 2 | Usar `v-html` o `dangerouslySetInnerHTML` |
| **Validación Backend** | Frontend solo envía datos, backend valida todo | Sin lógica de negocio compleja en cliente |
| **Feedback Inmediato** | Respuesta indica si continúa o termina | Mostrar mensaje basado en `decision` |
| **Datos Estructurados** | JSON listo para renderizar directamente | Mapear `texts[0].questions` a componentes |
| **Historial Persistente** | Todas las respuestas se guardan automáticamente | No necesita state management complejo |
| **Nivel Adaptativo** | Asignación basada en desempeño real | Personalizar experiencia post-diagnóstico |

---

## 💻 Ejemplos de Integración Frontend

### **Vue 3 - Componente de Diagnóstico**

```vue
<template>
  <div class="diagnostic-container">
    <!-- Loading State -->
    <div v-if="loading" class="loading">
      <p>Cargando diagnóstico...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
    </div>

    <!-- Diagnostic Content -->
    <div v-else>
      <div v-for="text in diagnosticTexts" :key="text.text_id" class="text-section">
        <h2>{{ text.title }}</h2>

        <!-- Renderizar según formato -->
        <div v-if="text.format === 'html'" 
             v-html="text.content" 
             class="html-content">
        </div>
        <div v-else class="plain-content">
          <p>{{ text.content }}</p>
        </div>

        <!-- Preguntas -->
        <div v-for="question in text.questions" 
             :key="question.question_id" 
             class="question-block">
          <p class="question-text">{{ question.question_text }}</p>

          <div class="alternatives">
            <label v-for="alt in question.alternatives" 
                   :key="alt.alternative_id"
                   class="alternative">
              <input 
                type="radio" 
                v-model="answers[question.question_id]"
                :name="`q${question.question_id}`" 
                :value="alt.alternative_id"
              />
              <span>{{ alt.text }}</span>
            </label>
          </div>
        </div>
      </div>

      <button @click="submitAnswers" 
              :disabled="!allQuestionsAnswered"
              class="btn-submit">
        Enviar Respuestas
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();
const props = defineProps({
  stage: {
    type: Number,
    required: true,
    validator: (value) => [1, 2].includes(value)
  },
  studentId: {
    type: String,
    required: true
  }
});

const diagnosticTexts = ref([]);
const answers = ref({});
const loading = ref(true);
const error = ref(null);

// Computed: Verificar si todas las preguntas están respondidas
const allQuestionsAnswered = computed(() => {
  const allQuestions = diagnosticTexts.value.flatMap(t => t.questions);
  return allQuestions.every(q => answers.value[q.question_id]);
});

// Cargar textos de diagnóstico
const loadTexts = async () => {
  try {
    loading.value = true;
    const response = await axios.get(
      `/api/v1/diagnostic/texts?stage=${props.stage}`
    );
    diagnosticTexts.value = response.data.texts;
  } catch (err) {
    error.value = `Error al cargar textos: ${err.response?.data?.detail || err.message}`;
    console.error(err);
  } finally {
    loading.value = false;
  }
};

// Enviar respuestas
const submitAnswers = async () => {
  try {
    const answersArray = Object.entries(answers.value).map(([qId, altId]) => ({
      question_id: parseInt(qId),
      alternative_id: altId
    }));

    const endpoint = props.stage === 1 
      ? '/api/v1/diagnostic/stage1' 
      : '/api/v1/diagnostic/stage2';

    const response = await axios.post(endpoint, {
      student_id: props.studentId,
      answers: answersArray
    });

    console.log('✅ Respuestas enviadas:', response.data);

    // Lógica según etapa
    if (props.stage === 1) {
      if (response.data.decision === 'CONTINUAR') {
        router.push(`/diagnostic/stage2?student_id=${props.studentId}`);
      } else {
        await assignLevel();
      }
    } else {
      await assignLevel();
    }
  } catch (err) {
    error.value = `Error al enviar respuestas: ${err.response?.data?.detail || err.message}`;
    console.error(err);
  }
};

// Asignar nivel final
const assignLevel = async () => {
  try {
    const response = await axios.post('/api/v1/diagnostic/assign-level', {
      student_id: props.studentId
    });

    console.log('✅ Nivel asignado:', response.data.assigned_level);
    router.push({
      name: 'DiagnosticComplete',
      params: { level: response.data.assigned_level }
    });
  } catch (err) {
    error.value = `Error al asignar nivel: ${err.response?.data?.detail || err.message}`;
    console.error(err);
  }
};

onMounted(() => {
  loadTexts();
});
</script>

<style scoped>
.diagnostic-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.text-section {
  margin-bottom: 3rem;
}

.html-content {
  margin: 1.5rem 0;
}

.plain-content {
  white-space: pre-wrap;
  line-height: 1.6;
  margin: 1.5rem 0;
}

.question-block {
  background: #f5f5f5;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
}

.question-text {
  font-weight: 600;
  margin-bottom: 1rem;
  color: #333;
}

.alternatives {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.alternative {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 4px;
  transition: background 0.2s;
}

.alternative:hover {
  background: rgba(0, 0, 0, 0.05);
}

.btn-submit {
  width: 100%;
  padding: 1rem;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-submit:hover:not(:disabled) {
  background: #45a049;
}

.btn-submit:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.loading, .error {
  text-align: center;
  padding: 2rem;
}

.error {
  color: #d32f2f;
}
</style>
```

---

### **React - Hook Personalizado**

```javascript
import { useState, useEffect } from 'react';
import axios from 'axios';

export const useDiagnostic = (stage, studentId) => {
  const [diagnosticTexts, setDiagnosticTexts] = useState([]);
  const [answers, setAnswers] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadTexts();
  }, [stage]);

  const loadTexts = async () => {
    try {
      setLoading(true);
      const response = await axios.get(
        `/api/v1/diagnostic/texts?stage=${stage}`
      );
      setDiagnosticTexts(response.data.texts);
    } catch (err) {
      setError(`Error al cargar textos: ${err.response?.data?.detail || err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const submitAnswers = async () => {
    try {
      const answersArray = Object.entries(answers).map(([qId, altId]) => ({
        question_id: parseInt(qId),
        alternative_id: altId
      }));

      const endpoint = stage === 1 
        ? '/api/v1/diagnostic/stage1' 
        : '/api/v1/diagnostic/stage2';

      const response = await axios.post(endpoint, {
        student_id: studentId,
        answers: answersArray
      });

      return response.data;
    } catch (err) {
      throw new Error(err.response?.data?.detail || err.message);
    }
  };

  const assignLevel = async () => {
    try {
      const response = await axios.post('/api/v1/diagnostic/assign-level', {
        student_id: studentId
      });
      return response.data;
    } catch (err) {
      throw new Error(err.response?.data?.detail || err.message);
    }
  };

  return {
    diagnosticTexts,
    answers,
    setAnswers,
    loading,
    error,
    submitAnswers,
    assignLevel
  };
};
```

---

## 🎯 Casos de Uso Principales

### **1. Onboarding de Nuevo Estudiante**
```
Usuario ingresa → Formulario de perfilamiento → POST /profiling 
→ Diagnóstico Etapa 1 → (Condicional) Etapa 2 → Asignación de nivel 
→ Dashboard personalizado
```

### **2. Re-evaluación de Estudiante Existente**
```
Dashboard → Botón "Realizar diagnóstico" → GET /texts?stage=1 
→ Flujo diagnóstico completo → Actualizar nivel
```

### **3. Modo Demo/Prueba**
```
Página de prueba → GET /texts?stage=1 (sin student_id) 
→ Mostrar textos sin guardar respuestas
```

---

## 🔒 Consideraciones de Seguridad

- ✅ Validación de `student_id` en cada endpoint
- ✅ Verificación de preguntas válidas por etapa
- ✅ Detección de respuestas duplicadas
- ✅ Protección contra inyección SQL (SQLAlchemy ORM)
- ⚠️ **Recomendación**: Implementar rate limiting en endpoints públicos

---

## 🚀 Próximos Pasos para el Frontend

1. **Implementar componentes reutilizables:**
   - `<DiagnosticQuestion />` para renderizar preguntas
   - `<TextRenderer />` para manejar HTML vs texto plano
   - `<ProgressBar />` para mostrar progreso (Etapa 1/2)

2. **Agregar animaciones/transiciones:**
   - Fade-in al cargar textos
   - Animación de progreso entre etapas
   - Celebración al completar diagnóstico

3. **Mejorar feedback visual:**
   - Indicador de respuestas seleccionadas
   - Contador de preguntas respondidas
   - Mensaje de confirmación antes de enviar

4. **Optimizaciones:**
   - Cache de textos en localStorage
   - Guardar progreso temporalmente
   - Recuperación de sesión interrumpida

---

## 📞 Soporte

Para más información sobre la implementación, consulta:
- `Documents/Frontend_Diagnostic_Integration.md` - Guía completa de integración
- `app/api/v1/diagnostic.py` - Endpoints implementados
- `app/schemas/diagnostic_schemas.py` - Esquemas de validación
