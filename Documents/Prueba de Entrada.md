Aquí tienes **una documentación clara, técnica y profesional** para que el **equipo web** pueda usar los endpoints del diagnóstico (F-02 y F-03).  
Incluye:  
✔ Explicación funcional  
✔ Cómo consumir cada endpoint  
✔ Ejemplos de request/response  
✔ En qué tablas se guarda la información  
✔ Flujo completo del diagnóstico

---

# 📘 **DOCUMENTACIÓN OFICIAL – Módulo de Diagnóstico (F-02, F-03)**

El módulo de diagnóstico sirve para determinar el **nivel de competencia inicial** de un estudiante mediante dos etapas:

- **F-02.A – Diagnóstico Etapa 1 (2 preguntas)**
    
- **F-02.B – Diagnóstico Etapa 2 (3 preguntas)**
    
- **F-03 – Asignación de nivel** según los resultados
    

---

# 📍 **1. Endpoints Disponibles**

| Etapa  | Método | Ruta                       | Descripción                                           |
| ------ | ------ | -------------------------- | ----------------------------------------------------- |
| F-02.A | POST   | `/diagnostic/stage1`       | Procesa 2 respuestas y decide si continúa o finaliza. |
| F-02.B | POST   | `/diagnostic/stage2`       | Procesa 3 respuestas después de superar Etapa 1.      |
| F-03   | POST   | `/diagnostic/assign-level` | Calcula nivel final y actualiza la tabla desempeño.   |

---

# 🗂️ **2. Tablas involucradas**

|Tabla|Se usa para|
|---|---|
|**usuario**|Identificar al estudiante vía `student_id`.|
|**alternativa**|Verificar si la alternativa seleccionada es correcta.|
|**resultado_diagnostico**|Guardar cada respuesta del estudiante.|
|**desempenio**|Guardar el nivel final asignado (F-03).|
|**grado**|Resolución del nivel en formato de grado.|

---

# 🧩 **3. Flujo completo del diagnóstico**

1️⃣ **Etapa 1 (2 preguntas)**  
→ Si responde las 2 correctamente → continúa  
→ Si falla alguna → asignación inmediata de nivel

2️⃣ **Etapa 2 (3 preguntas)**  
→ Solo si superó Etapa 1

3️⃣ **Asignación de nivel (F-03)**  
→ Se evalúan los resultados reales guardados en BD  
→ Se registra el nivel en la tabla `desempenio`

---

# 📝 **4. Endpoint 1 – Etapa 1 (F-02.A)**

### `POST /diagnostic/stage1`

## **Payload esperado**

```json
{
  "student_id": "1",
  "answers": [
    { "question_id": 1, "alternative_id": 10 },
    { "question_id": 2, "alternative_id": 12 }
  ]
}
```

### Validaciones

- Deben venir **exactamente 2 respuestas**
    
- `question_id` debe ser **1 o 2**
    
- Las alternativas deben existir en la tabla `alternativa`
    
- Se guarda en **resultado_diagnostico**
    

---

## **Respuesta (si todo ok):**

```json
{
  "student_id": "ABC123",
  "decision": "CONTINUAR",
  "correct_answers_count": 2,
  "message": "Diagnóstico Etapa 1 completado. Respuestas correctas: 2 de 2."
}
```

## **Dónde se guarda**

|Campo|Tabla|Descripción|
|---|---|---|
|id_usuario|resultado_diagnostico|Identifica usuario|
|id_pregunta|resultado_diagnostico|Pregunta respondida|
|id_alternativa_elegida|resultado_diagnostico|Alternativa elegida|
|es_correcta|resultado_diagnostico|Si la alternativa era correcta|
|fecha_respuesta|resultado_diagnostico|Timestamp|

---

# 📝 **5. Endpoint 2 – Etapa 2 (F-02.B)**

### `POST /diagnostic/stage2`

## **Payload esperado:**

```json
{
  "student_id": "1",
  "answers": [
    { "question_id": 3, "alternative_id": 1 },
    { "question_id": 4, "alternative_id": 2 },
    { "question_id": 5, "alternative_id": 3 }
  ]
}
```

### Validaciones

- Se requieren **exactamente 3 respuestas**
    
- Las preguntas deben ser **3,4,5**
    
- Las alternativas deben coincidir con la pregunta
    
- Se guarda en **resultado_diagnostico**
    

---

## **Respuesta**

```json
{
  "student_id": "ABC123",
  "correct_answers_count": 3,
  "message": "Diagnóstico Etapa 2 completado. Respuestas correctas: 3 de 3."
}
```

---

# 🎯 **6. Endpoint 3 – Asignación de nivel inicial (F-03)**

### `POST /diagnostic/assign-level`

Este endpoint:

✔ Obtiene los últimos resultados de Stage 1 y Stage 2  
✔ Verifica que sean del mismo intento (≤ 5 segundos)  
✔ Calcula el nivel final  
✔ Actualiza la tabla `desempenio`

---

## **Payload esperado**

```json
{
  "student_id": "1"
}
```

---

## **Lógica asignación de nivel**

### **Stage 1**

|Aciertos|Nivel|
|---|---|
|0|2do Grado|
|1|3er Grado|
|2|Pasar a Stage 2|

---

### **Stage 2**

|Aciertos|Nivel|
|---|---|
|0|3er Grado|
|1|4to Grado|
|2|5to Grado|
|3|6to Grado|

---

## **Respuesta**

```json
{
  "student_id": "ABC123",
  "assigned_level_label": "4to Grado",
  "assigned_level_grade": 4,
  "message": "Nivel de competencia inicial asignado exitosamente."
}
```

---

## **Dónde se guarda**

### Tabla: **desempenio**

|Campo|Descripción|
|---|---|
|id_usuario|Relación con estudiante|
|nivel|Ej: "4to Grado"|
|nivel_grado_id|ID en tabla grado|
|puntaje|Inicialmente 0|
|exactitud|0|
|promedio_tiempo_por_pregunta|0|
|promedio_tiempo_por_lectura|0|
|textos_considerados|0|

🔄 Si el usuario ya tiene un desempeño → **se actualiza**  
🆕 Si no tiene → **se crea** un nuevo registro

---

# 🧪 **7. Ejemplo completo (flujo)**

### 1) Etapa 1

POST `/diagnostic/stage1`  
→ Devuelve `"CONTINUAR"`

### 2) Etapa 2

POST `/diagnostic/stage2`

### 3) Asignación final

POST `/diagnostic/assign-level`  
→ Guarda nivel inicial

---

# 📌 **8. Indicaciones para el equipo web**

✔ Siempre llamar a los endpoints **en este orden**:

1. `/stage1`
    
2. si CONTINUAR → `/stage2`
    
3. `/assign-level`
    

✔ Los endpoints son **idempotentes por intento**  
✔ El frontend NO calcula nada, solo envía respuestas  
✔ Usar siempre los `id_pregunta` y `id_alternativa` reales de BD  
✔ El timestamp lo genera el backend automáticamente

---

# ✅ **Si deseas, puedo crearte:**

### ▫ Postman Collection

### ▫ Documentación en formato Swagger

### ▫ Diagramas de flujo

### ▫ Versión PDF o Notion-ready

¿Quieres alguno de estos?