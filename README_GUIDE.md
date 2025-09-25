# Guía de Desarrollo para Submódulos - Módulo de Recomendación y Evaluación

Este documento explica **cómo implementar un submódulo en FastAPI** dentro de este proyecto.
Cada integrante del equipo seguirá estos pasos para garantizar **coherencia, orden y facilidad de integración**.

---

## 📂 Dónde desarrollar

Cada submódulo debe implementar tres capas:

1. **Schemas** → `app/schemas/[submodulo]_schemas.py`

   - Definir los **modelos Pydantic** para entrada/salida de datos.
   - Ejemplo: `EvaluationInputRequest`, `EvaluationInputResponse`.
2. **Services** → `app/services/[submodulo]_service.py`

   - Aquí va la **lógica de negocio** del submódulo.
   - Debe recibir un objeto Pydantic y devolver otro objeto Pydantic.
   - Ejemplo: `EvaluationInputService.evaluate_student()`.
3. **API (rutas)** → `app/api/v1/[submodulo].py`

   - Aquí se define el endpoint público accesible desde otros módulos.
   - Usa `APIRouter` y conecta con el `service`.

Finalmente, registrar el router en:
`app/api/v1/router.py`

---

## 📡 Convenciones de Endpoints

- Usar prefijos descriptivos, ejemplo:
  - `/evaluation-input/`
  - `/evaluation-performance/`
  - `/recommendation-challenges/`
- Todas las rutas deben empezar con `/api/v1/`.

---

## ⚙️ Flujo de Integración

1. **Crear Schemas** → Definir modelos de entrada y salida.
2. **Crear Service** → Implementar la lógica principal.
3. **Crear API Router** → Exponer la ruta con `APIRouter`.
4. **Registrar en Router Global** (`app/api/v1/router.py`).
5. **Probar con FastAPI Docs** → Correr servidor y verificar en `http://127.0.0.1:8000/docs`.

---

## 🧪 Testing

- Cada submódulo debe tener su archivo de pruebas en:`app/tests/test_[submodulo].py`
- Se recomienda usar **pytest**.

Ejemplo:

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_evaluation_input():
    response = client.post("/api/v1/evaluation-input/", json={
        "student_id": "A123",
        "grade_level": 3,
        "preferences": ["animales"]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["initial_level"] in ["básico", "intermedio"]
```


## 📊 Buenas Prácticas

* Usar **Inyección de Dependencias** si en el futuro hay conexiones a BD.
* Mantener lógica compleja fuera de los routers (en `services/`).
* Usar nombres claros en variables y funciones.
* Documentar cada endpoint con docstrings.

---

## ☁️ Escalabilidad

* **Base de datos** : Ya existe `app/core/database.py` → usarlo si el submódulo necesita guardar datos.
* **Integraciones** : Conectar con otros equipos desde `app/integrations/`.
* **Nube** : Subida de resultados a cloud (ej. AWS, GCP, Azure) se maneja desde `integrations/cloud_storage.py`.

---

## ✅ Checklist al terminar un submódulo

* [ ] Schemas creados (`app/schemas/`).
* [ ] Service implementado (`app/services/`).
* [ ] API endpoint creado (`app/api/v1/`).
* [ ] Router registrado en `app/api/v1/router.py`.
* [ ] Test implementado (`app/tests/`).
* [ ] Documentado en `README_TEMPLATE.md`.
