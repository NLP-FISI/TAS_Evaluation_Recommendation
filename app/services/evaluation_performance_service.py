# app/services/evaluation_performance_service.py
from typing import List, Dict, Any
from app.core.database import get_conn, release_conn
from app.schemas.evaluation_performance import RegistroEvaluacionSalida, ResultadoEvaluacion

# ----- Repository: obtener registros crudos desde la BD -----
def get_raw_data_from_db(id_usuario: str) -> List[RegistroEvaluacionSalida]:
    """
    Lee los registros crudos desde la tabla que contiene los datos.
    Ajusta el nombre de la tabla/columnas si en tu BD se llaman distinto.
    """
    sql = """
        SELECT
            id_resultado_juego AS id_resultado_juego,
            tiempo_texto_seg AS tiempo_texto_seg,
            tiempo_pregunta_seg AS tiempo_pregunta_seg,
            correctas AS correctas,
            incorrectas AS incorrectas
        FROM performance_records 
        WHERE id_usuario = %s
        ORDER BY id ASC
    """
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=__import__("psycopg2.extras").extras.RealDictCursor) as cur:
            cur.execute(sql, (id_usuario,))
            rows = cur.fetchall()
            return [RegistroEvaluacionSalida(**r) for r in rows]
    finally:
        release_conn(conn)

# ----- Cálculo de métricas -----
def _compute_metrics(records: List[RegistroEvaluacionSalida]) -> Dict[str, Any]:
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
        "total_texts": total_texts,
        "total_questions": total_questions,
        "exactitud": exactitud,
        "promedio_tiempo_por_pregunta": promedio_tiempo_por_pregunta,
        "promedio_tiempo_por_lectura": promedio_tiempo_por_lectura
    }

# ----- Normalización de tiempos a score (0..1) -----
def _time_to_score(avg_time: float, expected: float) -> float:
    if avg_time <= 0:
        return 1.0
    s = 1.0 / (1.0 + (avg_time / expected))
    return max(0.0, min(1.0, s))

# ----- Fórmula ponderada (devuelve 0..100) -----
def _apply_weighted_formula(metrics: Dict[str, Any],
                            weight_exactitud: float = 0.7,
                            weight_time: float = 0.3,
                            expected_q: float = 30.0,
                            expected_r: float = 300.0) -> float:
    exactitud = metrics["exactitud"]  # 0..1
    q_score = _time_to_score(metrics["promedio_tiempo_por_pregunta"], expected_q)
    r_score = _time_to_score(metrics["promedio_tiempo_por_lectura"], expected_r)
    tiempo_combinado = 0.6 * q_score + 0.4 * r_score
    final = (exactitud * weight_exactitud + tiempo_combinado * weight_time) * 100.0
    return round(max(0.0, min(100.0, final)), 2)

# ----- Guardar resultado en tabla performance_evaluation -----
def _save_evaluation_to_db(id_usuario: str, result: Dict[str, Any]):
    sql = """
        INSERT INTO performance_results
            (id_usuario, puntaje, nivel, exactitud, promedio_tiempo_por_pregunta, promedio_tiempo_por_lectura, textos_considerados)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
    """
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (
                id_usuario,
                result["puntaje"],
                result["nivel"],
                result["exactitud"],
                result["promedio_tiempo_por_pregunta"],
                result["promedio_tiempo_por_lectura"],
                result["textos_considerados"]
            ))
            inserted_id = cur.fetchone()[0]
            conn.commit()
            return inserted_id
    finally:
        release_conn(conn)

# ----- Función principal: orquesta el flujo -----
def calculate_performance(id_usuario: str) -> ResultadoEvaluacion:
    records = get_raw_data_from_db(id_usuario)
    if not records:
        # devolver objeto vacío / o lanzar excepción según prefieras
        return ResultadoEvaluacion(
            id_usuario=id_usuario,
            puntaje=0.0,
            nivel="básico",
            exactitud=0.0,
            promedio_tiempo_por_pregunta=0.0,
            promedio_tiempo_por_lectura=0.0,
            textos_considerados=0
        )

    metrics = _compute_metrics(records)
    puntaje = _apply_weighted_formula(metrics)

    # asignar nivel
    if puntaje >= 80:
        nivel = "avanzado"
    elif puntaje >= 60:
        nivel = "intermedio"
    else:
        nivel = "básico"

    resultado = {
        "puntaje": puntaje,
        "nivel": nivel,
        "exactitud": round(metrics["exactitud"], 3),
        "promedio_tiempo_por_pregunta": round(metrics["promedio_tiempo_por_pregunta"], 2),
        "promedio_tiempo_por_lectura": round(metrics["promedio_tiempo_por_lectura"], 2),
        "textos_considerados": metrics["total_texts"]
    }

    # guardar en la tabla de evaluaciones (opcional)
    try:
        _save_evaluation_to_db(id_usuario, resultado)
    except Exception:
        # si falla el guardado, igual devolvemos el resultado. Loggear en producción.
        pass

    return ResultadoEvaluacion(
        id_usuario=id_usuario,
        puntaje=resultado["puntaje"],
        nivel=resultado["nivel"],
        exactitud=resultado["exactitud"],
        promedio_tiempo_por_pregunta=resultado["promedio_tiempo_por_pregunta"],
        promedio_tiempo_por_lectura=resultado["promedio_tiempo_por_lectura"],
        textos_considerados=resultado["textos_considerados"]
    )
