
# Evaluación de Retos

### Taller de Aplicaciones Sociales  
**Recomendación y Evaluación**  
**Versión:** 1.0  
**Módulo:** Evaluación de Retos  

---

## I. Introducción al Módulo

El módulo de **Evaluación de Retos** es el componente encargado de procesar los resultados de los desafíos competitivos entre estudiantes (duelos), determinar el ganador según criterios de precisión y velocidad, y actualizar el ranking de habilidades mediante un algoritmo **ELO**.

### Objetivo principal
Procesar automáticamente los resultados de retos gamificados, calcular el ganador y actualizar el ranking de los jugadores de manera justa y dinámica.

### Relación con otras partes del sistema
- **Módulo de Gamificación:** Envía los datos del reto completado para su evaluación.
- **Base de Datos PostgreSQL:** Almacena historial de retos y puntajes actualizados.
- **Sistema de Autenticación:** Verifica la identidad de los usuarios participantes.

---

## II. Alcance

### Funcionalidades incluidas
- Evaluación automática de los retos competitivos una vez finalizados.
- Determinación del ganador considerando precisión y tiempo.
- Actualización de puntuación mediante algoritmo **ELO**.
- Gestión de rachas de victorias y derrotas.
- Persistencia de resultados en base de datos.
- Generación de mensajes personalizados según rendimiento.

### Funcionalidades fuera de alcance
- Generación de preguntas para los retos.
- Emparejamiento de jugadores (matchmaking).
- Interfaz de usuario (front-end).
- Notificaciones en tiempo real.

---

## III. Requerimientos

### Requerimientos Funcionales

| Código | Descripción |
|--------|-------------|
| RF-01 | Procesar datos de retos completados (IDs, respuestas, tiempos) |
| RF-02 | Calcular puntaje bruto y aplicar desempate por tiempo |
| RF-03 | Calcular variación ELO |
| RF-04 | Persistir resultados en tablas Retos y Ranking |
| RF-05 | Gestionar eventos de abandono con penalización ELO |

### Requerimientos No Funcionales

| Código | Nombre | Descripción |
|--------|---------|--------------|
| RNF-01 | Rendimiento | Latencia de consulta < 50 ms |
| RNF-02 | Disponibilidad | Reintentos ante fallo de conexión |
| RNF-03 | Consistencia | Transacciones atómicas en BD |

---

## IV. Arquitectura y Diseño

El módulo utiliza una **arquitectura por capas** para asegurar claridad y escalabilidad.

### Capa de Exposición (API)
- Archivo: `evaluation_challenges.py`
- Expone el endpoint **POST `/api/v1/evaluation-challenges/`**
- Recibe el JSON y delega al servicio
- Valida datos con Pydantic

### Capa de Servicio (Lógica de Negocio)
- Archivo: `evaluation_challenges_service.py`
- Determina ganador, calcula ELO y aplica reglas (racha, empate, foto finish)
- Genera mensajes personalizados
- Prepara datos para persistencia en BD

### Capa de Esquemas (DTOs)
- Archivo: `challenges_schemas.py`
- Define estructuras de entrada/salida
- Valida tipos y formatos

### Capa de Persistencia
- Modelos SQLAlchemy (`app/models/`)
- Guarda variaciones de ELO, historial de retos y datos de usuario
- Mantiene integridad y trazabilidad

---

## V. Dependencias

### Librerías utilizadas
- FastAPI
- SQLAlchemy
- Pydantic
- pytest

### Servicios externos
- PostgreSQL

---

## VI. API

### Endpoint principal

```
POST /api/v1/evaluation-challenges/
```

### Descripción
Evalúa un reto competitivo entre dos jugadores y retorna ganador, variación ELO y mensajes personalizados.

### Ejemplo de Body (request)

```json
{
  "retador": {
    "id_usuario": 1,
    "respuestas_correctas": 8,
    "tiempo_total_seg": 120
  },
  "contrincante": {
    "id_usuario": 2,
    "respuestas_correctas": 6,
    "tiempo_total_seg": 130
  }
}
```

### Ejemplo de Response

```json
{
  "id_ganador": 1,
  "rating_anterior_retador": 1200,
  "rating_nuevo_retador": 1216,
  "variacion_retador": 16,
  "rating_anterior_contrincante": 1200,
  "rating_nuevo_contrincante": 1184,
  "variacion_contrincante": -16,
  "mensaje": "¡Muy bien! 👍"
}
```

---

## VII. Casos de Uso

### CU01: Victoria simple
Jugador con más respuestas correctas gana.

**Resultado:**  
- Ganador: Retador (ID 1)  
- Variación ELO: +16  
- Mensaje: "¡Muy bien! 👍"

---

### CU02: Victoria con racha “On Fire”
Jugador con 4 victorias consecutivas recibe bonus.

**Resultado:**  
- Variación ELO: 20 puntos  
- Mensaje: "¡Imparable! 🔥"

---

### CU03: Victoria rompiendo racha de derrotas (“remontada”)

**Resultado:**  
- Variación ELO: +26  
- Mensaje: "¡De vuelta al juego! 🚀"

---

### CU04: Empate Técnico
Ambos jugadores con mismos aciertos y tiempo.

**Resultado:**  
- Ganador: Ninguno  
- ELO: 0  
- Mensaje: "¡Empate! 🤝"

---

### CU05: Victoria por Foto Finish
Mismos aciertos, diferencia mínima de tiempo.

**Resultado:**  
- Ganador: Retador  
- ELO: +16  
- Mensaje: "¡Por un pelo! 🤏"

---

## VIII. Pruebas

### Suite principal
```
pytest app/tests/test_evaluation_challenges.py
```

### Casos cubiertos
- Victoria simple
- Racha “On Fire”
- Remontada
- Empate
- Foto Finish
- Cálculo de rachas

### Cobertura
- Determinación del ganador  
- Algoritmo ELO  
- Bonos por rachas  
- Persistencia en BD  
- Mensajes personalizados  
