# Módulo de Recomendación y Evaluación 📚🎮

Este proyecto forma parte de la **Plataforma Educativa Gamificada** de la Facultad de Ingeniería de Sistemas e Informática - UNMSM.
Nuestro equipo desarrolla el **módulo de Recomendación y Evaluación**, el cual provee servicios vía **APIs con FastAPI** para ser consumidos por los demás equipos del proyecto.

---

## 🚀 Objetivo del Módulo

Brindar servicios de **evaluación personalizada y recomendación adaptativa**, ajustados al nivel, desempeño y experiencia de los estudiantes de primaria.

---

## 🔑 Funcionalidades

- **Evaluación de Entrada**: Diagnóstico inicial del nivel del estudiante.
- **Evaluación de Desempeño**: Seguimiento del progreso y habilidades.
- **Recomendación de Retos**: Actividades y juegos adaptados.
- **Recomendación de Preguntas**: Preguntas de comprensión ajustadas.
- **Recomendación de Dificultad**: Ajuste dinámico del nivel de complejidad.
- **Recomendación de Usuarios**: Sugerencia de compañeros según nivel/experiencia.

---

## 🏗️ Arquitectura

- **Backend**: Python + FastAPI
- **Base de Datos**: PostgreSQL (extensible a MongoDB o Redis si se requiere)
- **Autenticación**: JWT Tokens (para comunicación segura entre módulos)
- **Despliegue**: Contenedores Docker (lista para escalar en la nube)

---

## 📂 Estructura de Carpetas

> Ver [aquí](README_TEMPLATE.md) la plantilla para documentar cada submódulo.

---

## ⚙️ Instalación

```bash
# Clonar repositorio
git clone <repo_url>
cd recommendation_evaluation_module

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Correr servidor local
uvicorn app.main:app --reload
$env:ENV="development"; uvicorn app.main:app --reload

# Verifica en el navegador:
👉 http://127.0.0.1:8000/docs (Swagger UI)
👉 http://127.0.0.1:8000/redoc (Redoc UI)
```

## 🧪 Testing

```
pytest app/tests/
```

---

## 📡 Endpoints Base

Todos los endpoints están bajo `/api/v1/`

Ejemplo:

```
POST /api/v1/evaluation-input/
POST /api/v1/recommendation-questions/
```

---

## 👥 Equipo

**Grupo de Recomendación y Evaluación - UNMSM**

Responsables del diseño y desarrollo del motor de recomendaciones y sistema de evaluación de la plataforma educativa.

---

## 📄 README_TEMPLATE.md (Plantilla para Submódulos)

```markdown
# [Nombre del Submódulo]

## 🎯 Objetivo
Describir en 2-3 líneas qué resuelve este submódulo.
---
## ⚙️ Funcionalidad

- [ ] Punto 1
- [ ] Punto 2
- [ ] Punto 3

---

## 📡 Endpoints

- `POST /api/v1/[ruta]/` → Explicación
- `GET /api/v1/[ruta]/` → Explicación

Ejemplo de Request:

```json
{
  "student_id": "1234",
  "nivel": "4to primaria",
  "preferencias": ["animales", "aventuras"]
}
```

## 🗃️ Modelos de Datos

* Modelo principal en `app/models/[archivo].py`
* Esquema en `app/schemas/[archivo].py`

---

## 🧪 Tests

* Ubicación: `app/tests/test_[submodulo].py`
* Ejemplo de prueba unitaria o de integración.

---

## 👥 Responsable

* Max Saavedra
