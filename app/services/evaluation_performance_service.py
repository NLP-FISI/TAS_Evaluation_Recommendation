from typing import List, Dict, Any, Optional
from app.core.database import get_db
from app.schemas.evaluation_performance import RegistroEvaluacionSalida, ResultadoEvaluacion
from sqlalchemy import text

PUNTOS_POR_PREGUNTA = 5

# Clasificación por nivel (según puntaje)
def obtener_nivel(puntaje: float) -> str:
    if puntaje >= 900:
        return "Muy Difícil"
    elif puntaje >= 600:
        return "Difícil"
    elif puntaje >= 300:
        return "Media"
    elif puntaje >= 150:
        return "Fácil"
    else:
        return "Muy Fácil"

# Obtener registros del usuario
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

# Calcular métricas
def calcular_metricas(records: List[RegistroEvaluacionSalida]) -> Dict[str, Any]:
    total_texts = len(records)
    total_correct = sum(r.correctas for r in records)
    total_incorrect = sum(r.incorrectas for r in records)
    total_questions = total_correct + total_incorrect
    
    total_questions_time = sum(r.tiempo_pregunta_seg for r in records)
    total_reading_time = sum(r.tiempo_texto_seg for r in records)

    promedio_tiempo_por_pregunta = (total_questions_time / total_questions) if total_questions > 0 else 0.0
    promedio_tiempo_por_lectura = (total_reading_time / total_texts) if total_texts > 0 else 0.0

    # Exactitud
    exactitud = (total_correct / total_questions) if total_questions > 0 else 0.0

    # Puntaje acumulado
    puntaje = total_correct * PUNTOS_POR_PREGUNTA

    return {
        "textos_considerados": total_texts,
        "correctas": total_correct,
        "incorrectas": total_incorrect,
        "puntaje": puntaje,
        "exactitud": round(exactitud, 3),
        "promedio_tiempo_por_pregunta": round(promedio_tiempo_por_pregunta, 2),
        "promedio_tiempo_por_lectura": round(promedio_tiempo_por_lectura, 2)
    }

# Guardar en BD
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
        nivel = obtener_nivel(metrics["puntaje"])

        resultado = {
            "id_usuario": id_usuario,
            "puntaje": metrics["puntaje"],
            "nivel": nivel,
            "exactitud": metrics["exactitud"],
            "promedio_tiempo_por_pregunta": metrics["promedio_tiempo_por_pregunta"],
            "promedio_tiempo_por_lectura": metrics["promedio_tiempo_por_lectura"],
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
