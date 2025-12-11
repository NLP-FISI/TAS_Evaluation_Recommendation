# Módulo de Evaluación de Desempeño  
### Taller de Aplicaciones Sociales  
**Cálculo de Rendimiento y Métricas del Usuario**  
**Versión:** 1.0  
**Módulo:** Evaluación de Desempeño

---

# I. Introducción al Módulo

El módulo de **Evaluación de Desempeño** se encarga de procesar el rendimiento histórico del usuario y generar un diagnóstico basado en métricas clave como:

- Porcentaje de aciertos  
- Tiempos promedio de lectura y resolución  
- Número total de textos evaluados  
- Comparación con el promedio general del sistema  

El objetivo es generar una clasificación automática del rendimiento del estudiante a partir de su historial de juegos registrados en la base de datos.

Este módulo se ejecuta cada vez que el cliente solicita evaluar a un usuario mediante la API.

## Objetivo principal
Procesar los registros del usuario, calcular sus métricas agregadas y asignar una categoría de desempeño (Excelente – Adecuado – Por mejorar), registrando el resultado actualizado en la BD.

## Relación con otras partes del sistema
- **Gamificación:** Permite mostrar al usuario su desempeño global.  
- **Módulo de Resultados del Juego:** Proporciona los datos base para el cálculo.  
- **Base de Datos PostgreSQL:** Guarda y actualiza el nivel de desempeño del usuario.  
- **Dashboard o UI:** Muestra los indicadores calculados.

---

# II. Alcance

## Funcionalidades incluidas
- Obtención del historial del usuario desde `resultado_juego`.  
- Cálculo de métricas agregadas (tiempos, aciertos, exactitud).  
- Comparación contra el promedio del sistema.  
- Clasificación del desempeño.  
- Persistencia de datos en la tabla `desempenio`.  
- Exposición mediante un endpoint FastAPI.

## Funcionalidades fuera de alcance
- Generar recomendaciones de dificultad.  
- Analizar preguntas individuales.  
- Predecir desempeño futuro.  
- Comparaciones entre usuarios o rankings.

---

# III. Requerimientos

## Requerimientos Funcionales

| Código | Descripción |
|--------|-------------|
| RF-01 | Obtener el historial de resultados del usuario |
| RF-02 | Calcular métricas agregadas (tiempos, aciertos, exactitud) |
| RF-03 | Obtener el promedio general del sistema |
| RF-04 | Clasificar el desempeño del usuario |
| RF-05 | Guardar o actualizar el registro de desempeño en BD |
| RF-06 | Devolver los resultados mediante API |

## Requerimientos No Funcionales

| Código | Nombre | Descripción |
|--------|---------|--------------|
| RNF-01 | Rendimiento | El cálculo debe ejecutarse en < 50 ms con historial promedio |
| RNF-02 | Robustez | Manejo adecuado de errores y transacciones |
| RNF-03 | Consistencia | Garantizar que la actualización del desempeño sea atómica |

---

# IV. Arquitectura y Diseño

El módulo utiliza una **arquitectura por capas**, separando datos, servicios y API.

## 1. Capa de Exposición (API)
- Archivo principal:  
  `evaluation_performance_router.py`
- Endpoint expuesto:  
  **POST `/performance/evaluate/{id_usuario}`**
- Responsable de:
  - recibir la solicitud,  
  - abrir conexión a BD,  
  - devolver el resultado validado con Pydantic.

## 2. Capa de Servicio (Lógica de Negocio)
Archivo:  
`evaluation_performance_service.py`

Implementa:
- Carga de registros desde BD  
- Cálculo de métricas globales  
- Clasificación del desempeño  
- Persistencia del resultado en tabla `desempenio`  

Funciones principales:
- `obtener_datos_bd`  
- `calcular_metricas`  
- `clasificar_desempenio`  
- `guardar_evaluacion`  
- `calcular_desempenio` (función central)

## 3. Capa de Esquemas (DTOs)
Archivo:  
`evaluation_performance.py`

Esquemas:
- `RegistroEvaluacionBase`  
- `RegistroEvaluacionSalida`  
- `SolicitudEvaluacion`  
- `ResultadoEvaluacion`  

## 4. Capa de Persistencia
- Modelo SQLAlchemy: `RegistroEvaluacion`  
- Tabla: `resultado_juego`  
- Esquema gestionado:
  - tiempos de lectura y preguntas  
  - correctas/incorrectas  
  - id del usuario  

El módulo también registra datos en tabla `desempenio` mediante consulta SQL.

---

# V. Dependencias

## Librerías utilizadas
- FastAPI  
- SQLAlchemy  
- Pydantic  
- psycopg2 (PostgreSQL)

## Servicios externos
- Base de datos PostgreSQL

---

# VI. API

## Endpoint principal

### **POST /performance/evaluate/{id_usuario}**

### Descripción
Procesa el historial del usuario y retorna:

- porcentaje de aciertos  
- tiempos promedio  
- total de textos considerados  
- categoría de desempeño  
- registro actualizado en la BD  

---

## Ejemplo de Response

```json
{
  "id_usuario": "15",
  "porcentaje_aciertos": 75.0,
  "promedio_tiempo_por_pregunta": 3.8,
  "promedio_tiempo_por_lectura": 12.5,
  "textos_considerados": 4,
  "desempeño": "Desempeño adecuado"
}
```

## VII. Casos de Uso

- **CU01: Usuario con alto rendimiento**  
  El usuario mantiene altas tasas de acierto.  
  **Resultado:**  
  Exactitud ≥ 0.8  
  **Categoría:** Excelente desempeño

- **CU02: Usuario con rendimiento promedio**  
  El usuario se mantiene cerca del promedio general.  
  **Resultado:**  
  Exactitud entre 0.6 y 0.8  
  **Categoría:** Desempeño adecuado

- **CU03: Usuario con bajo rendimiento**  
  El usuario tiene más errores que aciertos.  
  **Resultado:**  
  Exactitud < 0.6  
  **Categoría:** Por mejorar

- **CU04: Usuario sin registros**  
  El usuario aún no tiene historial en `resultado_juego`.  
  **Resultado:**  
  La API retorna 404  
  No se genera evaluación

## VIII. Flujo General del Proceso

1. El cliente llama al endpoint.  
2. El servicio obtiene los registros del usuario.  
3. Se calculan métricas agregadas.  
4. Se guarda o actualiza el registro en `desempenio`.  
5. Se retorna la evaluación completa.

