import numpy as np
import pandas as pd
from faker import Faker
from sklearn.cluster import KMeans
import random

fake = Faker()

# -----------------------------
# Generar datos fake al iniciar
# -----------------------------


def generar_datos_usuarios(n=100):
    ciclos = ["Primaria", "Secundaria", "Universitario"]
    data = []

    for i in range(n):
        desempeno = np.clip(np.random.normal(75, 15), 0, 100)
        consistencia = np.clip(np.random.normal(70, 20), 0, 100)
        diversificacion = np.clip(np.random.normal(60, 25), 0, 100)
        ciclo = random.choice(ciclos)
        tiempo_promedio = np.clip(np.random.normal(120, 30), 30, 240)

        nivel_experiencia = (0.5 * desempeno) + \
            (0.3 * consistencia) + (0.2 * diversificacion)

        data.append({
            "user_id": i + 1,
            "nombre": fake.first_name(),
            "ciclo": ciclo,
            "desempeno": round(desempeno, 2),
            "consistencia": round(consistencia, 2),
            "diversificacion": round(diversificacion, 2),
            "tiempo_promedio": round(tiempo_promedio, 2),
            "nivel_experiencia": round(nivel_experiencia, 2)
        })

    return pd.DataFrame(data)


def entrenar_kmeans(df, n_clusters=4):
    X = df[["nivel_experiencia", "tiempo_promedio"]]
    model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df["cluster"] = model.fit_predict(X)
    return df, model


# Entrenamiento inicial (data fake cargada al iniciar FastAPI)
df_usuarios, modelo_kmeans = entrenar_kmeans(
    generar_datos_usuarios(), n_clusters=4)


# -----------------------------
# Función de recomendación
# -----------------------------
def recomendar_oponentes(user_id: int, dificultad: str = "equilibrado"):
    df = df_usuarios.copy()

    if user_id not in df["user_id"].values:
        return {"error": "Usuario no encontrado."}

    usuario = df[df["user_id"] == user_id].iloc[0]
    mismo_cluster = df[df["cluster"] == usuario["cluster"]]
    mismo_cluster = mismo_cluster[mismo_cluster["user_id"] != user_id]
    mismo_cluster["diff_exp"] = abs(
        mismo_cluster["nivel_experiencia"] - usuario["nivel_experiencia"])
    mismo_cluster = mismo_cluster.sort_values(by="diff_exp")

    if dificultad == "fácil":
        recomendados = mismo_cluster[mismo_cluster["nivel_experiencia"]
                                     < usuario["nivel_experiencia"]].head(3)
    elif dificultad == "desafiante":
        recomendados = mismo_cluster[mismo_cluster["nivel_experiencia"]
                                     > usuario["nivel_experiencia"]].head(3)
    else:
        recomendados = mismo_cluster.head(3)

    return {
        "usuario_base": {
            "user_id": int(usuario["user_id"]),
            "nombre": usuario["nombre"],
            "nivel_experiencia": float(usuario["nivel_experiencia"]),
            "cluster": int(usuario["cluster"])
        },
        "recomendaciones": recomendados[["user_id", "nombre", "nivel_experiencia", "cluster"]].to_dict(orient="records")
    }
