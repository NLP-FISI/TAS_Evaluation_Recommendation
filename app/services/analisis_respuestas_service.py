# app/services/analisis_respuestas_service.py
import pandas as pd
from sqlalchemy import func, Integer
from app.core.database import SessionLocal
from app.models.respuesta_usuario import RespuestaUsuario
from app.models.pregunta import Pregunta  # Debe tener campo tipo_pregunta


def analizar_desempenio_usuario(user_id: int):
    """
    Analiza las respuestas registradas por un usuario para detectar
    en qué tipo de preguntas presenta más fallas o fortalezas.
    """
    db = SessionLocal()

    # Consultamos las respuestas del usuario y su tipo de pregunta
    resultados = (
        db.query(
            Pregunta.tipo_pregunta,
            func.count(RespuestaUsuario.id_respuesta).label("total"),
            func.sum(func.cast(RespuestaUsuario.es_correcta, Integer)
                     ).label("correctas")
        )
        .join(Pregunta, Pregunta.id_pregunta == RespuestaUsuario.id_pregunta)
        .filter(RespuestaUsuario.id_usuario == user_id)
        .group_by(Pregunta.tipo_pregunta)
        .all()
    )

    db.close()

    if not resultados:
        return {"mensaje": "No hay respuestas registradas para este usuario."}

    # Procesamos los resultados en DataFrame para análisis
    df = pd.DataFrame(resultados, columns=[
                      "tipo_pregunta", "total", "correctas"])
    df["correctas"] = df["correctas"].fillna(0)
    df["incorrectas"] = df["total"] - df["correctas"]
    df["porcentaje_acierto"] = round((df["correctas"] / df["total"]) * 100, 2)

    tipo_mas_fallado = df.loc[df["porcentaje_acierto"].idxmin(),
                              "tipo_pregunta"]
    tipo_mas_acertado = df.loc[df["porcentaje_acierto"].idxmax(
    ), "tipo_pregunta"]

    return {
        "usuario": user_id,
        "resumen": {
            "total_preguntas": int(df["total"].sum()),
            "total_correctas": int(df["correctas"].sum()),
            "total_incorrectas": int(df["incorrectas"].sum()),
            "tipo_mas_fallado": tipo_mas_fallado,
            "tipo_mas_acertado": tipo_mas_acertado
        },
        "detalle_por_tipo": df.to_dict(orient="records")
    }
