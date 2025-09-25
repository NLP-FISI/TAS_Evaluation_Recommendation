## 📁 Estructura de Carpetas

```
recommendation_evaluation_module/
├── README.md                  # Documentación general del módulo
├── README_TEMPLATE.md         # Plantilla para que cada submódulo documente su propósito
├── pyproject.toml             # Configuración de dependencias (Poetry) o requirements.txt si prefieren pip
├── requirements.txt         
├── alembic/                   # Migraciones de base de datos
│   ├── env.py
│   ├── versions/
│   └── README.md
├── app/
│   ├── main.py                # Punto de entrada FastAPI
│   ├── config.py              # Configuración (DB, env vars, etc.)
│   ├── core/                  # Core del sistema (utilidades y base para todos los módulos)
│   │   ├── database.py        # Conexión a la base de datos
│   │   ├── security.py        # JWT, auth, permisos (si aplica)
│   │   └── utils.py           # Funciones utilitarias comunes
│   ├── api/                   # Endpoints (rutas de la API organizadas por submódulos)
│   │   ├── v1/              
│   │   │   ├── __init__.py
│   │   │   ├── evaluation_input.py       # Evaluación de entrada
│   │   │   ├── evaluation_performance.py # Evaluación de desempeño
│   │   │   ├── recommendation_challenges.py   # Recomendación de retos
│   │   │   ├── recommendation_questions.py    # Recomendación de preguntas
│   │   │   ├── recommendation_difficulty.py   # Recomendación de dificultad
│   │   │   ├── recommendation_users.py        # Recomendación de usuarios por nivel/experiencia
│   │   │   └── router.py              # Punto unificado de rutas
│   ├── services/              # Lógica de negocio (cada submódulo aquí)
│   │   ├── evaluation_input_service.py
│   │   ├── evaluation_performance_service.py
│   │   ├── recommendation_challenges_service.py
│   │   ├── recommendation_questions_service.py
│   │   ├── recommendation_difficulty_service.py
│   │   └── recommendation_users_service.py
│   ├── models/                # Modelos de BD (SQLAlchemy / Pydantic)
│   │   ├── __init__.py
│   │   ├── evaluation.py
│   │   └── recommendation.py
│   ├── schemas/               # Esquemas de validación con Pydantic
│   │   ├── __init__.py
│   │   ├── evaluation_schemas.py
│   │   └── recommendation_schemas.py
│   ├── tests/                 # Tests unitarios y de integración
│   │   ├── __init__.py
│   │   ├── test_evaluation.py
│   │   └── test_recommendation.py
│   └── integrations/          # Integraciones con otros módulos/equipos o servicios externos
│       ├── __init__.py
│       ├── cloud_storage.py   # Si suben resultados o reportes a la nube
│       └── external_api.py    # Conexión a otros módulos vía API
└── scripts/                   # Scripts útiles (ej: carga inicial de datos, seeds)
    ├── seed_data.py
    └── export_reports.py

```
