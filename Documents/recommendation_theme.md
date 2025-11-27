
# Documentación del Módulo de Recomendación de Temática

## I. Introducción al Módulo

El módulo de Recomendación de Temática permite sugerir una temática adecuada para un usuario basándose en similitud con otros usuarios que ya tienen asignada una temática.

El modelo utiliza un enfoque basado en aprendizaje no supervisado mediante el algoritmo K-Nearest Neighbors (KNN), entrenado en memoria y sin persistencia en disco.

---

## II. Alcance

Este módulo cubre:

* Obtención de usuarios con temáticas asignadas.
* Construcción de una matriz de características para análisis de similitud.
* Entrenamiento de un modelo KNN en memoria.
* Recomendación de una temática según la similitud entre usuarios.
* Exposición del servicio mediante un endpoint REST.

No cubre:

* Persistencia de modelos.
* Criterios avanzados de recomendación.
* Manejo de grandes volúmenes de datos o procesamiento distribuido.

---

## III. Requerimientos

* Python 3.10+
* FastAPI
* SQLAlchemy
* scikit-learn
* NumPy
* Base de datos con información de usuarios y temáticas

---

## IV. Arquitectura y Diseño

### Capa de Exposición (API)

Archivo: `app/api/recommendation_tematica_router.py`

Responsabilidades:

* Recibir solicitudes HTTP.
* Validar existencia del usuario.
* Llamar al servicio de recomendación.
* Construir la respuesta serializada.

### Capa de Servicio (Lógica de Negocio)

Archivo: `app/services/recommendation_tematica_service.py`

Responsabilidades:

* Obtener datos relevantes de la BD.
* Crear matriz de características.
* Entrenar modelo KNN en memoria.
* Calcular similitudes entre usuarios.
* Seleccionar temática recomendada.

### Capa de Esquemas (DTOs)

No se implementan DTOs específicos para este módulo.

Los datos son devueltos directamente como diccionario plano desde el endpoint.

### Capa de Persistencia

Modelos involucrados:

* `Usuario`
* `Tematica`

Operaciones:

* Obtener usuarios con temática asignada.
* Obtener usuario objetivo.
* Obtener la temática final recomendada.

---

## V. Dependencias

### Dependencias internas

* `app.models.usuario.Usuario`
* `app.models.tematica.Tematica`
* `app.core.database.get_db`

### Dependencias externas

* `fastapi`
* `sqlalchemy`
* `numpy`
* `sklearn.neighbors.NearestNeighbors`

---

## VI. API

### Endpoint Principal

**GET /tematica/recomendar/{user_id}**

Descripción:

Retorna la temática recomendada para un usuario basándose en similitud con otros usuarios existentes.

### Ejemplo de Request

Sin body, solo parámetro de ruta:

`GET /tematica/recomendar/12`

### Ejemplo de Response

```json
{
    "id_tematica": 3,
    "nombre_tematica": "Ciencia"
}
```

### Lógica Interna Simplificada

1. Buscar usuarios con temática asignada.
2. Construir matriz de características: edad, puntos, monedas.
3. Entrenar modelo KNN en memoria.
4. Obtener usuario objetivo.
5. Buscar vecinos más cercanos.
6. Seleccionar temática más frecuente entre ellos.

---

## VII. Casos de Uso

### Caso 1: Usuario con datos suficientes

El usuario tiene edad, puntos y monedas registrados.

Existen usuarios similares con temáticas asignadas.

Resultado: se devuelve una temática recomendada.

### Caso 2: Usuario sin datos de desempeño

El usuario existe pero carece de información necesaria.

Resultado: no se encuentra temática y se devuelve error 404.

### Caso 3: No existen usuarios con temática asignada

No hay dataset para entrenar el modelo.

Resultado: no se puede recomendar y se devuelve error 404.

### Caso 4: Temáticas empatadas

Si varias temáticas se repiten con la misma frecuencia, se selecciona una por orden de aparición.

---

## VIII. Pruebas

### Pruebas Unitarias Recomendadas

1. Prueba de recomendación válida
   * Crear usuarios simulados con temáticas asignadas.
   * Verificar que el usuario objetivo recibe una temática válida.
2. Prueba sin usuarios con temática
   * La función debe retornar None.
   * El endpoint debe responder 404.
3. Prueba de usuario inexistente
   * El endpoint debe responder 404.
4. Prueba de valores nulos
   * Usuarios con edad/puntos/monedas nulos deben ser convertidos a 0 sin errores.
5. Prueba de consistencia
   * Mismo input debe producir misma recomendación.

Si deseas, puedo generarte  **los tests en pytest listos para ejecutar** .
