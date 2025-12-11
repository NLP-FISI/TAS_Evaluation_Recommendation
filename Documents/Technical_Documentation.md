# Documentación Técnica del Proyecto: Módulo de Recomendación y Evaluación

## Índice
1. [Introducción](#introducción)
2. [Arquitectura General](#arquitectura-general)
3. [Estructura de Carpetas](#estructura-de-carpetas)
4. [Dependencias y Configuración](#dependencias-y-configuración)
5. [Descripción de Componentes Principales](#descripción-de-componentes-principales)
    - [API y Ruteo](#api-y-ruteo)
    - [Modelos de Datos](#modelos-de-datos)
    - [Servicios](#servicios)
    - [Esquemas (Schemas)](#esquemas-schemas)
    - [Core y Configuración](#core-y-configuración)
6. [Base de Datos](#base-de-datos)
7. [Ejecución y Pruebas](#ejecución-y-pruebas)
8. [Despliegue y Docker](#despliegue-y-docker)
9. [Equipo y Contacto](#equipo-y-contacto)

---

## Introducción
Este módulo forma parte de la Plataforma Educativa Gamificada de la Facultad de Ingeniería de Sistemas e Informática - UNMSM. Provee servicios de evaluación personalizada y recomendación adaptativa mediante APIs desarrolladas en FastAPI.

## Arquitectura General
- **Backend:** Python 3.10+ con FastAPI
- **Base de Datos:** PostgreSQL (SQLAlchemy ORM)
- **Autenticación:** JWT Tokens
- **Despliegue:** Docker

## Estructura de Carpetas
```
app/
  api/           # Rutas y controladores de la API
  core/          # Configuración, utilidades y conexión a BD
  integrations/  # Integraciones externas (APIs, almacenamiento)
  models/        # Modelos ORM (SQLAlchemy)
  schemas/       # Esquemas Pydantic para validación
  services/      # Lógica de negocio y servicios
  tests/         # Pruebas unitarias y de integración
alembic/         # Migraciones de base de datos
Documents/       # Documentos técnicos y funcionales
scripts/         # Scripts de utilidad y entrenamiento
```

## Dependencias y Configuración
- **Dependencias principales:**
  - fastapi, uvicorn, SQLAlchemy, pydantic, psycopg2-binary, numpy, pandas, scikit-learn, joblib, python-dotenv, requests, httpx
- **Gestión de dependencias:** `requirements.txt`
- **Variables de entorno:** `.env` (usuario, contraseña, host, puerto y nombre de la BD)
- **Configuración:** `app/core/config.py` y `app/core/database.py`

## Descripción de Componentes Principales

### API y Ruteo
- **`app/main.py`**: Inicializa la aplicación FastAPI, configura CORS y monta el router principal bajo `/api/v1`.
- **`app/api/v1/router.py`**: Agrega y organiza todos los endpoints de la API (evaluación, recomendación, diagnóstico, etc.).

### Modelos de Datos
- **Ubicación:** `app/models/`
- **Descripción:** Modelos ORM (SQLAlchemy) que representan las tablas principales: Usuario, Pregunta, Texto, Alternativa, Grado, Desempeño, Resultado, etc.
- **Ejemplo:**
  - `Usuario`: Datos del estudiante, preferencias, desempeño, etc.
  - `Pregunta`: Preguntas asociadas a textos, dificultad y tipo.
  - `Texto`: Textos de lectura para diagnóstico y evaluación.
  - `Alternativa`: Opciones de respuesta para cada pregunta.

### Servicios
- **Ubicación:** `app/services/`
- **Descripción:** Lógica de negocio, procesamiento de datos, generación de recomendaciones, análisis de respuestas, etc.
- **Ejemplo:**
  - `recommendation_input_service.py`: Genera textos y preguntas de entrada para diagnóstico.
  - `evaluation_performance_service.py`: Procesa y evalúa el desempeño del usuario.
  - `recommendation_difficulty_service.py`: Ajusta la dificultad de los retos y preguntas.

### Esquemas (Schemas)
- **Ubicación:** `app/schemas/`
- **Descripción:** Esquemas Pydantic para validación y serialización de datos de entrada/salida en la API.

### Core y Configuración
- **`app/core/config.py`**: Carga variables de entorno y construye la URL de conexión a la base de datos.
- **`app/core/database.py`**: Inicializa el motor y la sesión de SQLAlchemy, provee la dependencia para endpoints.
- **`app/core/utils.py`**: Funciones utilitarias generales.

## Base de Datos
- **ORM:** SQLAlchemy
- **Migraciones:** Alembic (`alembic/`)
- **Tablas principales:** usuario, pregunta, texto, alternativa, grado, dificultad, resultado, etc.
- **Relaciones:**
  - Un usuario tiene preferencias (temáticas), grado, desempeño, resultados.
  - Una pregunta pertenece a un texto, tiene alternativas, dificultad y tipo.
  - Un texto tiene preguntas, dificultad, temática y tipo.

## Ejecución y Pruebas
- **Ejecución local:**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  pip install -r requirements.txt
  uvicorn app.main:app --reload
  ```
- **Documentación interactiva:**
  - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
  - Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- **Pruebas:**
  ```bash
  pytest app/tests/
  ```

## Despliegue y Docker
- **Dockerfile:** Incluido en la raíz del proyecto para despliegue en contenedores.
- **Variables de entorno:** Se deben definir en el entorno de despliegue o en un archivo `.env`.
- **Comando de despliegue:**
  ```bash
  docker build -t recommendation-evaluation .
  docker run -d -p 8000:8000 --env-file .env recommendation-evaluation
  ```

## Equipo y Contacto
- **Grupo de Recomendación y Evaluación - UNMSM**
- **Responsable técnico:** Max Saavedra
- **Contacto:** [Agregar correo o medio de contacto]

---

> Para detalles de cada submódulo, revisar los archivos en `Documents/` y la plantilla `README_TEMPLATE.md`.
