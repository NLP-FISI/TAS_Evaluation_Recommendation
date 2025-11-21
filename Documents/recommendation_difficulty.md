# Módulo de Recomendación de Dificultad
### Taller de Aplicaciones Sociales  
**Recomendación y Evaluación**  
**Versión:** 1.0  
**Módulo:** Recomendación de Dificultad  

---

# I. Introducción al Módulo

El módulo de **Recomendación de Dificultad** es responsable de ajustar dinámicamente el nivel de dificultad asignado a un usuario durante su experiencia en actividades gamificadas. Utiliza un **modelo híbrido basado en la Teoría de Respuesta al Ítem (IRT)**, lo que permite adaptar los retos futuros en función de su desempeño acumulado y reciente.

Este mecanismo permite que cada estudiante reciba desafíos con un nivel adecuado, personalizado y progresivo.

Debe ejecutarse cada que se termina un nivel para que el siguiente nivel se tenga una (dificultad_acumulada) actualizada

## Objetivo principal
Actualizar la habilidad acumulada del usuario (θ) y determinar la dificultad recomendada del siguiente reto (β), basándose en su rendimiento y la dificultad promedio de los textos o actividades anteriores.

## Relación con otras partes del sistema
- **Gamificación:** Proporciona al juego un valor de dificultad entre 1-5.
- **Base de Datos PostgreSQL:** Registra la dificultad acumulada del usuario.
- **Módulo de Recomendación de Textos:** Utiliza la dificultad estimada para seleccionar textos adecuados al nivel del usuario.

---
# II. Alcance

## Funcionalidades incluidas
- Actualización de la habilidad acumulada del usuario (θ).
- Cálculo de la probabilidad esperada de éxito mediante modelo **IRT–Rasch**.
- Gestión de racha de aciertos/errores.
- Cálculo de la dificultad recomendada para el siguiente reto.
- Persistencia de cambios en la base de datos.

## Funcionalidades fuera de alcance
- Generación de contenido o textos recomendados.
- Evaluación de duelos multiusuario.
- Cálculo de ranking entre estudiantes.

---

# III. Requerimientos

## Requerimientos Funcionales

| Código | Descripción |
|--------|-------------|
| RF-01 | Obtener rendimiento del usuario en un juego específico |
| RF-02 | Calcular probabilidad de éxito mediante modelo IRT |
| RF-03 | Actualizar dificultad acumulada |
| RF-04 | Determinar la recomendación de dificultad para el siguiente juego |
| RF-05 | Persistir cambios en la base de datos |

## Requerimientos No Funcionales

| Código | Nombre | Descripción |
|--------|---------|--------------|
| RNF-01 | Rendimiento | La actualización debe ejecutarse en < 50 ms |
| RNF-02 | Disponibilidad | Manejo robusto de errores y transacciones seguras |
| RNF-03 | Consistencia | Cambios atómicos sobre el modelo Usuario |

---

# IV. Arquitectura y Diseño

El módulo implementa una **arquitectura por capas**, garantizando separación de responsabilidades, facilidad de pruebas y mantenibilidad.

## 1. Capa de Exposición (API)
- Archivo principal:  
  `recommendation_difficulty_api.py`  
- Expone el endpoint:  
  **POST `/recommendation/difficulty/update`**
- Validación de entrada mediante Pydantic (`UpdateDifficultyRequest`)
- Conexión a la base de datos mediante `Depends(get_db)`

## 2. Capa de Servicio (Lógica de Negocio)
- Archivo:  
  `recommendation_difficulty_service.py`
- Implementa:  
  - Modelo IRT (cálculo de probabilidad)
  - Actualización
  - Factor de racha (estático)
  - Generación de dificultad recomendada (β siguiente)

## 3. Capa de Esquemas (DTOs)
- Archivo: `recommendation_schemas.py`
- Esquemas:  
  - `UpdateDifficultyRequest`  
  - `LastTextRequest`  
  - `TextComplexityRequest`  
  - `TextComplexityResponse`

## 4. Capa de Persistencia
- Modelos SQLAlchemy en `app/models/`
- Entidad principal: **Usuario**
- Campos gestionados:  
  - `dificultad_acumulada`  
- Garantiza integridad mediante transacciones

---

# V. Dependencias

## Librerías utilizadas
- FastAPI  
- SQLAlchemy ORM  
- Pydantic  
- psycopg2 (PostgreSQL)  
- pytest (pruebas)

## Servicios externos
- Base de Datos PostgreSQL

---

# VI. API

## Endpoint principal
POST /recommendation/difficulty/update
### Descripción
Calcula el nuevo valor de dificultad acumulada de un usuario (θ), basándose en:

- su rendimiento reciente,
- la dificultad promedio del contenido previo,
- la probabilidad prevista por el modelo IRT.

También retorna la dificultad recomendada del siguiente juego (β siguiente).

---

## Ejemplo de Body Request

```json
{
  "id_usuario": 15,
  "id_juego": 3
}
```
## Ejemplo de Response
```json
{
  "id_usuario": 15,
  "id_juego": 3,
  "dificultad_acumulada_anterior": 2.7,
  "dificultad_acumulada_actualizada": 3.02,
  "promedio_dificultad_juego": 3.0,
  "recomendacion_de_dificultad": 3,
  "correctas": 6,
  "incorrectas": 2,
  "resultado": 1
}
```

# VII. Casos de Uso

## CU01: Actualización tras acierto simple
El usuario acierta y supera la dificultad promedio del contenido.

**Resultado:**
- θ aumenta ligeramente  
- β sugerido incrementa o se mantiene  

---


## CU02: Actualización tras error
Un resultado incorrecto reduce la habilidad estimada.

**Resultado:**
- θ disminuye  
- β sugerido puede bajar  

---

## CU03: Usuario con habilidad estabilizada
Si la probabilidad esperada coincide con el rendimiento.

**Resultado:**
- θ cambia mínimamente  
- Sistema converge hacia un nivel adecuado  

---

## CU04: Sin historial previo (No esta planificado debido al examen de entrada)
Usuario sin valores previos en `dificultad_acumulada`.

**Resultado:**
- θ inicial = 1  
- Actualización según primer resultado  
