import numpy as np
import pandas as pd
from sqlalchemy.orm import Session
from sklearn.neighbors import NearestNeighbors
from app.core.database import SessionLocal
from app.models.usuario import Usuario
from app.models.grado import Grado
from app.models.desempenio import Desempenio


def obtener_datos_usuarios(db: Session):
    """
    Carga desde la BD los usuarios con sus características principales.
    """
    query = (
        db.query(
            Usuario.id_usuario,
            Usuario.nombre_usuario,
            Usuario.edad,
            Usuario.puntos,
            Usuario.monedas,
            Usuario.id_grado,
            Desempenio.puntaje,
            Desempenio.exactitud,
            Desempenio.promedio_tiempo_por_pregunta,
            Grado.ciclo_grado
        )
        .join(Desempenio, Usuario.id_usuario == Desempenio.id_usuario)
        .join(Grado, Usuario.id_grado == Grado.id_grado)
        .filter(Usuario.activo == True)
        .all()
    )

    df = pd.DataFrame(query, columns=[
        "id_usuario", "nombre_usuario", "edad", "puntos", "monedas", "id_grado",
        "puntaje", "exactitud", "promedio_tiempo_por_pregunta", "ciclo_grado"
    ])

    # Normalizamos valores faltantes
    df = df.fillna(0)
    return df


def recomendar_oponentes(user_id: int, dificultad: str = "equilibrado"):
    db = SessionLocal()
    df = obtener_datos_usuarios(db)
    db.close()

    if user_id not in df["id_usuario"].values:
        return {"error": "Usuario no encontrado."}

    # Seleccionamos al usuario base
    usuario = df[df["id_usuario"] == user_id].iloc[0]

    # Filtramos usuarios del mismo grado
    mismo_grado = df[df["id_grado"] == usuario["id_grado"]]
    mismo_grado = mismo_grado[mismo_grado["id_usuario"] != user_id]

    if mismo_grado.empty:
        return {"mensaje": "No hay oponentes disponibles en el mismo grado."}

    # Seleccionamos características numéricas para KNN
    features = ["puntaje", "exactitud",
                "promedio_tiempo_por_pregunta", "puntos", "monedas"]
    X = mismo_grado[features].values
    user_vector = usuario[features].values.reshape(1, -1)

    # Entrenamos un modelo KNN para medir similitud
    knn = NearestNeighbors(n_neighbors=min(5, len(mismo_grado)))
    knn.fit(X)
    distances, indices = knn.kneighbors(user_vector)

    # Ajustamos el rango de dificultad
    if dificultad == "fácil":
        idx = indices[0][-3:]  # oponentes más débiles (más lejos)
    elif dificultad == "desafiante":
        idx = indices[0][:3]   # oponentes más fuertes (más cerca)
    else:  # equilibrado
        mid = len(indices[0]) // 2
        idx = indices[0][max(0, mid-1):mid+2]

    recomendados = mismo_grado.iloc[idx]

    return {
        "usuario_base": {
            "id_usuario": int(usuario["id_usuario"]),
            "nombre": usuario["nombre_usuario"],
            "grado": int(usuario["id_grado"]),
            "puntaje": int(usuario["puntaje"]),
            "exactitud": int(usuario["exactitud"])
        },
        "recomendaciones": recomendados[[
            "id_usuario", "nombre_usuario", "puntaje", "exactitud", "puntos", "monedas"
        ]].to_dict(orient="records")
    }
