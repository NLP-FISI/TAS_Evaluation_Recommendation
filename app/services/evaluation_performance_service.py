from typing import List, Dict, Any, Optional
from app.core.database import get_db
from app.schemas.evaluation_performance import RegistroEvaluacionSalida, ResultadoEvaluacion
import math
from sqlalchemy import text

ALPHA_EXACTITUD = 0.7  # Peso de la Precisión (alpha)
BETA_TIEMPO = 0.3      # Peso de T_norm (beta)
W1_PREGUNTA = 0.6      # Peso de Tp_norm
W2_LECTURA = 0.4       # Peso de tl_norm

#si el P90 de la BD es NULL, cero o negativo se usan estos valores
MIN_TREF_P = 30.0 
MIN_TREF_R = 200.0

def obtener_datos_bd(db, id_usuario: str) -> List[RegistroEvaluacionSalida]:
    sql = text("""
        SELECT
            id_resultado_juego,
            id_usuario,
            tiempo_texto_seg,
            tiempo_pregunta_seg,
            correctas,
            incorrectas
        FROM resultado_juego
        WHERE id_usuario = :id_usuario
        ORDER BY id_resultado_juego ASC
    """)
   
    rows = db.execute(sql, {"id_usuario": id_usuario}).mappings().all()
    # Convertir id_resultado_juego a str
    return [
        RegistroEvaluacionSalida(
            id_resultado_juego=str(r['id_resultado_juego']),
            id_usuario=id_usuario,
            tiempo_texto_seg=r['tiempo_texto_seg'],
            tiempo_pregunta_seg=r['tiempo_pregunta_seg'],
            correctas=r['correctas'],
            incorrectas=r['incorrectas']
        )
        for r in rows
    ]
# Obtener referencias grupales (P90)
def obtener_tiempo_referencias_db(db) -> Dict[str, float]:
    sql = text("""
        SELECT
            percentile_cont(0.9) WITHIN GROUP (ORDER BY tiempo_pregunta_seg) AS tref_p,
            percentile_cont(0.9) WITHIN GROUP (ORDER BY tiempo_texto_seg) AS tref_r
        FROM resultado_juego
    """)
    references = db.execute(sql).mappings().first()

    tref_p_db = references.get('tref_p') if references else None
    tref_r_db = references.get('tref_r') if references else None

    final_tref_p = tref_p_db if tref_p_db and tref_p_db > 0 else MIN_TREF_P
    final_tref_r = tref_r_db if tref_r_db and tref_r_db > 0 else MIN_TREF_R

    return {"tref_p": final_tref_p, "tref_r": final_tref_r}


# Calcular métricas
def calcular_metricas(records: List[RegistroEvaluacionSalida]) -> Dict[str, Any]:
    total_texts = len(records)
    total_correct = sum(r.correctas for r in records)
    total_incorrect = sum(r.incorrectas for r in records)
    total_questions_time = sum(r.tiempo_pregunta_seg for r in records)
    total_reading_time = sum(r.tiempo_texto_seg for r in records)

    total_questions = total_correct + total_incorrect

    exactitud = (total_correct / total_questions) if total_questions > 0 else 0.0
    promedio_tiempo_por_pregunta = (total_questions_time / total_questions) if total_questions > 0 else 0.0
    promedio_tiempo_por_lectura = (total_reading_time / total_texts) if total_texts > 0 else 0.0

    return {
        "textos_considerados": total_texts,
        "exactitud": exactitud,
        "promedio_tiempo_por_pregunta": promedio_tiempo_por_pregunta,
        "promedio_tiempo_por_lectura": promedio_tiempo_por_lectura
    }


# Normalización de tiempos (Tp_norm y tl_norm) 
#Convierte el tiempo promedio a una eficiencia (0..1) 
def normalizar_tiempo(prom_time: float, tref: float) -> float:
   
    if prom_time is None or prom_time <= 0:
        # si no hay datos validos entonces retornamos eficiencia neutra 0.5
        return 0.5
    
    # Ratio = t_usuario / t_referencia
    ratio = prom_time / tref

    time_norm = 1.0 - min(ratio, 1.0)
    
    return time_norm

# Calcular formula_principal y Puntaje 
def calcular_formula_principal(metrics: Dict[str, Any],
                             tref_p: float,
                             tref_r: float,
                             alpha: float = ALPHA_EXACTITUD,
                             beta: float = BETA_TIEMPO,
                             w1: float = W1_PREGUNTA,
                             w2: float = W2_LECTURA) -> float:
        
    precision = metrics["exactitud"] 

    #Normalizar tiempos individuales (Tp_norm y tl_norm)
    tp_norm = normalizar_tiempo(metrics["promedio_tiempo_por_pregunta"], tref_p)
    tl_norm = normalizar_tiempo(metrics["promedio_tiempo_por_lectura"], tref_r)
    
    #Combinar tiempos normalizados (T_norm)
    t_norm = (w1 * tp_norm) + (w2 * tl_norm)
    
    #Calcular la Formula Principal (0..1)
    formula_principal = (precision * alpha) + (t_norm * beta)
    
    #Escalar a Puntaje (0..100) y redondear
    puntaje = round(formula_principal * 100.0, 2)
    
    return puntaje

# Guardar resultado
def guardar_evaluacion(db, result: Dict[str, Any]):
    sql = text("""
        INSERT INTO desempenio
            (id_usuario, puntaje, nivel, exactitud, promedio_tiempo_por_pregunta, 
             promedio_tiempo_por_lectura, textos_considerados)
        VALUES (:id_usuario, :puntaje, :nivel, :exactitud, :promedio_tiempo_por_pregunta,
                :promedio_tiempo_por_lectura, :textos_considerados)
        ON CONFLICT (id_usuario) DO UPDATE 
        SET 
            puntaje = EXCLUDED.puntaje, 
            nivel = EXCLUDED.nivel,
            exactitud = EXCLUDED.exactitud,
            promedio_tiempo_por_pregunta = EXCLUDED.promedio_tiempo_por_pregunta,
            promedio_tiempo_por_lectura = EXCLUDED.promedio_tiempo_por_lectura,
            textos_considerados = EXCLUDED.textos_considerados;
    """)
    db.execute(sql, result)
    db.commit()

# Función principal
def calcular_desempenio(id_usuario: str) -> Optional[ResultadoEvaluacion]:
    from app.core.database import SessionLocal
    db = SessionLocal()
    try:
        records = obtener_datos_bd(db, id_usuario)
        if not records:
            return None

        metrics = calcular_metricas(records)
        references = obtener_tiempo_referencias_db(db)
        puntaje = calcular_formula_principal(metrics, references["tref_p"], references["tref_r"])

        if puntaje >= 80:
            nivel = "avanzado"
        elif puntaje >= 60:
            nivel = "intermedio"
        else:
            nivel = "básico"

        resultado = {
            "id_usuario": id_usuario,
            "puntaje": puntaje,
            "nivel": nivel,
            "exactitud": round(metrics["exactitud"], 3),
            "promedio_tiempo_por_pregunta": round(metrics["promedio_tiempo_por_pregunta"], 2),
            "promedio_tiempo_por_lectura": round(metrics["promedio_tiempo_por_lectura"], 2),
            "textos_considerados": metrics["textos_considerados"]
        }

        guardar_evaluacion(db, resultado)

        return ResultadoEvaluacion(**resultado)
    except Exception as e:
        print(f"ERROR crítico en calcular_desempenio para {id_usuario}: {e}")
        db.rollback()
        return None
    finally:
        db.close()
