
# Módulo de Recomendación de Usuarios

## I. Introducción al Módulo

El módulo Recommendation Users proporciona un sistema de recomendación de oponentes utilizando un modelo de similitud basado en K-Nearest Neighbors (KNN).

Este sistema compara estadísticas del usuario con otros del mismo grado académico para sugerir oponentes adecuados según el nivel de dificultad solicitado: fácil, equilibrado o desafiante.

---

## II. Alcance

El alcance del módulo incluye:

* Exposición de un endpoint REST para obtener recomendaciones de usuarios.
* Lógica de negocio para procesar datos y generar sugerencias.
* Conexión a la base de datos para obtener características relevantes de los usuarios.
* Normalización, filtrado y aplicación del algoritmo KNN.
* Retorno de recomendaciones basadas en dificultad.

No incluye:

* Gestión o creación de usuarios.
* Modificación de datos de desempeño.
* Entrenamiento avanzado de modelos de machine learning.

---

## III. Requerimientos

### Requerimientos Técnicos

* Python 3.10+
* FastAPI
* SQLAlchemy
* scikit-learn
* Pandas
* NumPy
* Base de datos con tablas:
  * Usuario
  * Grado
  * Desempenio

### Requerimientos Funcionales

* El sistema debe aceptar un `user_id` válido.
* Debe recomendar hasta 5 usuarios del mismo grado académico.
* Debe aceptar un parámetro de dificultad: fácil, equilibrado, desafiante.
* Debe retornar los usuarios más adecuados según similitud.

---

## IV. Arquitectura y Diseño

### Capa de Exposición (API)

Archivo: `app/api/v1/recommendation_users.py`

* Define el endpoint principal:
  ```
  GET /recommendation/users/{user_id}
  ```
* Parámetros:
  * `user_id` (path)
  * `difficulty` (query param con valores permitidos: "fácil", "equilibrado", "desafiante")
* Delegación directa al servicio `recomendar_oponentes`.

---

### Capa de Servicio (Lógica de Negocio)

Funciones principales:

1. **obtener_datos_usuarios(db)**
   * Obtiene desde la base de datos las características de los usuarios.
   * Une tablas: Usuario, Desempenio, Grado.
   * Devuelve un DataFrame estandarizado.
2. **recomendar_oponentes(user_id, dificultad)**
   * Carga todos los usuarios y selecciona al usuario base.
   * Filtra por usuarios activos y del mismo grado.
   * Prepara un vector de características:
     * puntaje
     * exactitud
     * promedio_tiempo_por_pregunta
     * puntos
     * monedas
   * Aplica KNN para medir similitud.
   * Selecciona usuarios según dificultad.

---

### Capa de Esquemas (DTOs)

Actualmente los datos retornados se generan de forma manual sin Pydantic.

Puede ser mejorado implementando modelos DTO para:

* Usuario base
* Recomendación de oponentes
* Respuestas de error

---

### Capa de Persistencia

Se utiliza SQLAlchemy para conectarse y consultar la base de datos:

* Usuario
* Desempenio
* Grado

Conexión obtenida mediante:

```python
from app.core.database import SessionLocal
```

La consulta se realiza con joins y se transforma a DataFrame para manipulación eficiente.

---

## V. Dependencias

Dependencias externas:

```
fastapi
sqlalchemy
pandas
numpy
scikit-learn
uvicorn
```

Dependencias internas:

* app.models.usuario.Usuario
* app.models.grado.Grado
* app.models.desempenio.Desempenio
* app.core.database.SessionLocal

---

## VI. API

### Endpoint Principal

```
GET /recommendation/users/{user_id}
```

### Parámetros

| Nombre     | Tipo | Ubicación | Opciones                        | Descripción                |
| ---------- | ---- | ---------- | ------------------------------- | --------------------------- |
| user_id    | int  | path       | -                               | ID del usuario base         |
| difficulty | str  | query      | fácil, equilibrado, desafiante | Nivel de dificultad deseado |

---

### Ejemplo de Request

```
GET /recommendation/users/10?difficulty=equilibrado
```

### Ejemplo de Body (request)

Este endpoint no recibe body; solo parámetros en path y query.

---

### Ejemplo de Response

```json
{
  "usuario_base": {
    "id_usuario": 10,
    "nombre": "Juan Perez",
    "grado": 3,
    "puntaje": 820,
    "exactitud": 87
  },
  "recomendaciones": [
    {
      "id_usuario": 14,
      "nombre_usuario": "Carlos Ruiz",
      "puntaje": 810,
      "exactitud": 85,
      "puntos": 1200,
      "monedas": 340
    },
    {
      "id_usuario": 18,
      "nombre_usuario": "Ana Torres",
      "puntaje": 830,
      "exactitud": 90,
      "puntos": 1500,
      "monedas": 400
    }
  ]
}
```

---

## VII. Casos de Uso

### Caso 1: Solicitud de recomendación equilibrada

* Entrada: `GET /recommendation/users/25?difficulty=equilibrado`
* Resultado: lista de usuarios de rendimiento similar.

### Caso 2: Solicitud de oponentes más débiles

* difficulty = `fácil`
* Resultado: usuarios más distantes en el espacio de características.

### Caso 3: Solicitud de oponentes desafiantes

* difficulty = `desafiante`
* Se devuelven los usuarios más similares al usuario base.

### Caso 4: Usuario no encontrado

Respuesta:

```json
{"error": "Usuario no encontrado."}
```

### Caso 5: No existe nadie del mismo grado

Respuesta:

```json
{"mensaje": "No hay oponentes disponibles en el mismo grado."}
```

---

## VIII. Pruebas

### Pruebas Unitarias Recomendadas

| Prueba                    | Objetivo                                                |
| ------------------------- | ------------------------------------------------------- |
| Carga correcta de datos   | Validar estructura del DataFrame obtenido               |
| Usuario inexistente       | Validar respuesta de error                              |
| Filtrado por grado        | Confirmar que solo se incluyan usuarios del mismo grado |
| Ejecución del modelo KNN | Verificar integridad de cálculos                       |
| Dificultad: fácil        | Debe retornar los usuarios más lejanos                 |
| Dificultad: desafiante    | Debe retornar los usuarios más cercanos                |
| Dificultad: equilibrado   | Debe tomar un rango intermedio                          |
| Estructura del response   | Validar campos esperados                                |

### Pruebas del Endpoint (con TestClient)

* `GET /recommendation/users/1`
* `GET /recommendation/users/1?difficulty=fácil`
* `GET /recommendation/users/1?difficulty=desafiante`

### Pruebas de rendimiento

* Evaluar tiempo de respuesta
* Evaluar comportamiento con grandes volúmenes de usuarios
* Optimización del uso de DataFrames y consultas SQL
