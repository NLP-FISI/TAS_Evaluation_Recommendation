
# Módulo de Recomendación de Tipo de Texto

## I. Introducción al Módulo

El módulo Recommendation Text Type proporciona un sistema de recomendación del tipo de texto más adecuado para cada usuario.

El sistema recibe un identificador de usuario, obtiene sus características desde la base de datos y utiliza un modelo de recomendación para sugerir un tipo de texto (narrativo, argumentativo, descriptivo, expositivo, etc.).

Este módulo permite entrenar o cargar un modelo durante la inicialización del router y expone un endpoint para obtener la recomendación final.

---

## II. Alcance

Este módulo cubre:

* Exposición del endpoint REST para predecir el tipo de texto recomendado.
* Lógica de negocio para aplicar reglas o modelos de recomendación.
* Posibilidad de utilizar un modelo real basado en machine learning sin persistirlo.
* Consulta directa a la base de datos para obtener información del usuario.
* Retorno del tipo de texto recomendado (id y nombre).

No incluye:

* Creación o modificación de tipos de texto.
* Persistencia de modelos entrenados.
* Análisis semántico avanzado del comportamiento del usuario.

---

## III. Requerimientos

### Requerimientos Técnicos

* Python 3.10+
* FastAPI
* SQLAlchemy
* scikit-learn (opcional, para mejorar el modelo)
* Base de datos con:
  * Usuario
  * TipoTexto

### Requerimientos Funcionales

* El sistema debe cargar o simular un modelo durante el inicio.
* El endpoint debe devolver un objeto con:
  * id_tipo_texto
  * nombre_tipo_texto
* Debe manejar adecuadamente errores (usuario no encontrado).
* El modelo no debe persistirse en disco.

---

## IV. Arquitectura y Diseño

### Capa de Exposición (API)

Archivo: `app/api/v1/recommendation_text_type.py`

* Define el endpoint principal:
  ```
  GET /recommendation-text-type/{user_id}
  ```
* Entrena/carga el modelo al momento de inicializar el router:
  ```python
  entrenar_modelo_tipo_texto()
  ```
* Obtiene usuario desde la BD y delega al servicio para obtener la recomendación.

---

### Capa de Servicio (Lógica de Negocio)

Funciones principales:

1. **entrenar_modelo_tipo_texto()**
   * Actualmente simula la carga del modelo.
   * Puede mejorarse utilizando un clasificador simple de scikit-learn entrenado en memoria sin guardarse.
2. **recomendar_tipo_texto(usuario, db)**
   * Implementa la lógica de recomendación basada en:
     * edad
     * puntos
     * género
   * Si no coincide con ninguna regla, selecciona un tipo aleatorio.
   * Consulta la BD para obtener el registro real del tipo de texto.

---

### Capa de Esquemas (DTOs)

El módulo retorna un diccionario con:

```json
{
  "id_tipo_texto": number,
  "nombre_tipo_texto": string
}
```

Puede mejorarse definiendo modelos Pydantic para mayor claridad y validación.

---

### Capa de Persistencia

El módulo utiliza SQLAlchemy para:

* Buscar el usuario según id
* Buscar tipos de texto existentes
* Retornar la recomendación desde la tabla TipoTexto

---

## V. Dependencias

Dependencias externas:

```
fastapi
sqlalchemy
scikit-learn (opcional, para modelo real)
```

Dependencias internas:

* app.models.usuario.Usuario
* app.models.tipo_texto.TipoTexto
* app.core.database.get_db

---

## VI. API

### Endpoint Principal

```
GET /recommendation-text-type/{user_id}
```

### Parámetros

| Nombre  | Tipo | Ubicación | Descripción                                   |
| ------- | ---- | ---------- | ---------------------------------------------- |
| user_id | int  | path       | ID del usuario que recibirá la recomendación |

---

### Ejemplo de Request

```
GET /recommendation-text-type/12
```

---

### Ejemplo de Response

```json
{
  "tipo_texto_recomendado": {
    "id_tipo_texto": 3,
    "nombre_tipo_texto": "Narrativo"
  }
}
```

---

## VII. Casos de Uso

### Caso 1: Usuario menor de 10 años

Resultado esperado:

Tipo de texto narrativo.

### Caso 2: Usuario con más de 1000 puntos

Resultado esperado:

Tipo argumentativo.

### Caso 3: Usuario mujer sin condiciones previas

Resultado esperado:

Tipo descriptivo.

### Caso 4: Usuario que no cumple reglas

Resultado esperado:

Selección aleatoria entre:

* Expositivo
* Informativo
* Dialogado
* Poético

### Caso 5: Usuario inexistente

Respuesta:

```json
{"detail": "Usuario no encontrado"}
```

---

## VIII. Pruebas

### Pruebas Unitarias Recomendadas

| Prueba                 | Objetivo                                                      |
| ---------------------- | ------------------------------------------------------------- |
| Usuario no encontrado  | Debe retornar HTTP 404                                        |
| Elección por edad     | Validar que menores de 10 reciben "Narrativo"                 |
| Elección por puntos   | Validar que usuarios con >1000 puntos reciben "Argumentativo" |
| Elección por género  | Si género = F y no hay otras reglas, retornar "Descriptivo"  |
| Selección aleatoria   | Validar que el resultado pertenece al conjunto permitido      |
| Resultado existe en BD | Validar que se devuelve un tipo existente                     |

### Pruebas del Endpoint

* `GET /recommendation-text-type/1`
* Simular género femenino
* Simular puntos altos
* Probar usuarios pequeños de edad
