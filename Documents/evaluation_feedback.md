### 🧩 **Módulo: Generación de Feedback por Resultado de Juego**

**Versión:** 1.0  
**Proyecto:** Taller de Aplicaciones Sociales  
**Componente:** Recomendación y Evaluación  

---

##  **I. Introducción al Módulo**

El módulo de **Generación de Feedback** analiza los resultados de una partida (respuestas correctas e incorrectas) y genera un mensaje personalizado basado en el desempeño del estudiante.

###  **Objetivo principal**
Interpretar el rendimiento del usuario y generar un mensaje motivacional según su porcentaje de aciertos.

###  **Relación con otros componentes**
-  **Resultados de Juego:** Proporciona el ID a evaluar.  
-  **Base de Datos PostgreSQL:** Almacena correctas/incorrectas.  
-  **Gamificación:** Puede usar este feedback como refuerzo.  

---

##  **II. Alcance**

###  **Funcionalidades incluidas**
- Lectura del resultado usando **id_resultado_juego**.  
- Cálculo del **porcentaje de aciertos**.  
- Generación de **mensaje personalizado**.  
- Manejo de errores **404**.  
- Retorno de **JSON estructurado**.

###  **Fuera de alcance**
- Registro de partidas.  
- Algoritmos ELO o rachas.  
- Front-end.  
- Notificaciones.  

---

##  **III. Requerimientos**

###  **Requerimientos Funcionales**

| **Código** | **Descripción** |
|-----------|------------------|
| **RF-01** | Leer correctas/incorrectas desde la BD. |
| **RF-02** | Calcular porcentaje de aciertos. |
| **RF-03** | Generar mensaje según desempeño. |
| **RF-04** | Devolver JSON con la evaluación. |

### ⚙️ **Requerimientos No Funcionales**

| **Código** | **Nombre** | **Descripción** |
|-----------|-------------|------------------|
| **RNF-01** | Rendimiento | Tiempo de respuesta < 50 ms. |
| **RNF-02** | Disponibilidad | Manejo seguro de errores de BD. |
| **RNF-03** | Consistencia | Acceso controlado con SQLAlchemy. |

---

##  **IV. Arquitectura y Diseño**

El módulo usa una **arquitectura modular por capas**.

###  **Capa de Exposición (API)**
- Archivo: `feedback.py`  
- Endpoint: `POST /api/v1/feedback`  
- Recibe **id_resultado_juego**.  
- Maneja excepciones.  

###  **Capa de Servicio**
- Calcula porcentaje.  
- Selecciona mensaje.  
- Retorna datos formateados.  

###  **Capa de Persistencia**
- Modelo SQLAlchemy: **ResultadoJuego**.  
- Obtiene datos desde PostgreSQL.  

---

##  **V. Dependencias**

###  **Librerías**
- FastAPI  
- SQLAlchemy  
- Pydantic  
- pytest  

###  **Servicios externos**
- PostgreSQL  

---

##  **VI. API**

###  **Endpoint principal**
`POST /api/v1/feedback?id_resultado_juego=#`

###  **Ejemplo de Response**
```json
{
  "id_resultado_juego": 5,
  "correctas": 7,
  "incorrectas": 3,
  "porcentaje": 70.0,
  "mensaje": "Muy buen desempeño, sigue así 💪"
}
