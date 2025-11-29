
# Módulo de Clasificación de Tiers

## I. Introducción al Módulo

El módulo Classification Tiers implementa un sistema de categorización automática de usuarios utilizando un modelo de Machine Learning entrenado en memoria.

El modelo se basa en métricas de desempeño de los usuarios para asignar un nivel o tier (Principiante, Intermedio, Avanzado, Experto).

Este sistema entrena un modelo temporal con datos reales provenientes de la base de datos, evitando cualquier persistencia en disco.

---

## II. Alcance

El módulo abarca:

* Exposición de un endpoint REST para clasificar usuarios según sus métricas.
* Entrenamiento temporal de un modelo de clasificación con los datos disponibles en la base de datos.
* Transformación de los datos en un DataFrame para su uso en modelos.
* Categorización en tiers según puntaje.
* Retorno de un objeto estructurado con métricas y tier asignado.

Este módulo no incluye:

* Persistencia de modelos entrenados.
* Análisis avanzado de desempeño.
* Administración o edición de los tiers.
* Visualización de estadísticas.

---

## III. Requerimientos

### Requerimientos Técnicos

* Python 3.10+
* FastAPI
* SQLAlchemy
* pandas
* scikit-learn
* Motor de base de datos compatible con SQLAlchemy

### Requerimientos Funcionales

* Cargar todos los registros de desempeño desde la base de datos.
* Clasificar usuarios utilizando un modelo de Machine Learning entrenado al vuelo.
* Validar existencia de usuario y de métricas antes de clasificar.
* Retornar siempre el tier asignado junto con la información del usuario.

---

## IV. Arquitectura y Diseño

### Capa de Exposición (API)

Archivo:

`app/api/v1/recommendation_tiers.py`

Responsabilidades:

* Exponer el endpoint:
  ```
  GET /tiers/{user_id}
  ```
* Validar la existencia del usuario.
* Convertir los registros del modelo Desempenio en un DataFrame.
* Generar etiquetas de tier según el nivel de experiencia.
* Preparar el diccionario user_data para clasificación.
* Delegar en el servicio la asignación final del tier.

---

### Capa de Servicio (Lógica de Negocio)

Archivo:

`app/services/recommendation_tiers_service.py`

Funciones principales:

#### 1. entrenar_y_clasificar(df_entrenamiento, user_data)

* Recibe el DataFrame completo con registros históricos.
* Prepara los features:
  * nivel_experiencia
  * consistencia
  * tiempo_promedio
  * diversificacion
* Entrena un modelo `RandomForestClassifier()` en memoria.
* Clasifica al usuario con las métricas proporcionadas.
* Devuelve un diccionario con:
  * id del usuario
  * nombre
  * métricas
  * tier asignado

Este modelo nunca se guarda en disco, garantizando solo uso temporal.

---

### Capa de Esquemas (DTOs)

El endpoint retorna un objeto con la forma:

```json
{
  "usuario": {
    "user_id": number,
    "nombre": string,
    "nivel_experiencia": number,
    "consistencia": number,
    "tiempo_promedio": number,
    "diversificacion": number,
    "tier_asignado": "Principiante" | "Intermedio" | "Avanzado" | "Experto"
  }
}
```

---

### Capa de Persistencia

Utiliza SQLAlchemy para:

* Obtener información desde:
  * Usuario
  * Desempenio
* Convertir los registros en un DataFrame apto para entrenamiento.
* Recuperar métricas específicas del usuario para la predicción.

No se almacena ningún modelo.

---

## V. Dependencias

Dependencias internas:

* app.services.recommendation_tiers_service
* app.models.usuario.Usuario
* app.models.desempenio.Desempenio
* app.core.database.get_db

Dependencias externas:

```
fastapi
sqlalchemy
pandas
scikit-learn
```

---

## VI. API

### Endpoint Principal

```
GET /tiers/{user_id}
```

### Parámetros

| Nombre  | Tipo | Ubicación | Descripción                |
| ------- | ---- | ---------- | --------------------------- |
| user_id | int  | path       | ID del usuario a clasificar |

---

### Ejemplo de Request

```
GET /tiers/15
```

---

### Ejemplo de Response

```json
{
  "usuario": {
    "user_id": 15,
    "nombre": "Juan Pérez",
    "nivel_experiencia": 72,
    "consistencia": 85,
    "tiempo_promedio": 110,
    "diversificacion": 40,
    "tier_asignado": "Avanzado"
  }
}
```

---

## VII. Casos de Uso

### Caso 1: Usuario sin métricas registradas

El endpoint debe responder:

```json
{"detail": "No hay datos de desempeño para este usuario."}
```

### Caso 2: Base de datos sin registros de desempeño

Respuesta:

```json
{"detail": "No hay registros de desempeño en la base de datos."}
```

### Caso 3: Usuario con nivel_experiencia <= 30

Tier esperado: Principiante

### Caso 4: Usuario entre 31 y 60

Tier esperado: Intermedio

### Caso 5: Usuario entre 61 y 85

Tier esperado: Avanzado

### Caso 6: Usuario mayor de 85

Tier esperado: Experto

### Caso 7: Entrenamiento temporal exitoso

El modelo RandomForestClassifier debe crearse en memoria y destruirse al finalizar.

---

## VIII. Pruebas

### Pruebas Unitarias Recomendadas

| Prueba                                    | Objetivo                                         |
| ----------------------------------------- | ------------------------------------------------ |
| Clasificar usuario con métricas válidas | Verificar cálculo correcto del tier             |
| Usuario inexistente                       | Validar error 404                                |
| Desempeños vacíos                       | Validar error 404                                |
| Usuario sin desempeño                    | Debe lanzar error                                |
| Validación de DataFrame                  | Confirmar estructura correcta para entrenamiento |
| Reentrenamiento continuo                  | Comprobar que siempre se entrena en memoria      |

### Pruebas del Endpoint

* `GET /tiers/1`
* Usuario con diferentes valores de puntaje
* Simular jugador experto
* Validar formato de respuesta

---

Si quieres, puedo generar:

* Un README general para tu repositorio.
* Diagramas UML para estos módulos.
* Pruebas unitarias en pytest.
* Un documento consolidado con todos los módulos de recomendación.
