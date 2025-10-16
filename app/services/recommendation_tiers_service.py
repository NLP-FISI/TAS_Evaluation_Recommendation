# app/services/recommendation_tiers_service.py
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
from faker import Faker

fake = Faker()

def generar_datos_entrenamiento(n=300):
    data = []
    for _ in range(n):
        experiencia = np.clip(np.random.normal(60, 20), 0, 100)
        consistencia = np.clip(np.random.normal(70, 15), 0, 100)
        tiempo_promedio = np.clip(np.random.normal(120, 30), 30, 240)
        diversificacion = np.clip(np.random.normal(65, 25), 0, 100)

        # Etiquetamos según la experiencia (rango)
        if experiencia <= 30:
            tier = "Principiante"
        elif experiencia <= 60:
            tier = "Intermedio"
        elif experiencia <= 85:
            tier = "Avanzado"
        else:
            tier = "Experto"

        data.append({
            "nivel_experiencia": experiencia,
            "consistencia": consistencia,
            "tiempo_promedio": tiempo_promedio,
            "diversificacion": diversificacion,
            "tier": tier
        })

    return pd.DataFrame(data)


def entrenar_modelo_tiers():
    df = generar_datos_entrenamiento()
    X = df[["nivel_experiencia", "consistencia", "tiempo_promedio", "diversificacion"]]
    y = df["tier"]

    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)

    os.makedirs("app/fake_model", exist_ok=True)
    joblib.dump(model, "app/fake_model/tiers_model.pkl")
    return model


def cargar_modelo_tiers():
    path = "app/fake_model/tiers_model.pkl"
    if not os.path.exists(path):
        return entrenar_modelo_tiers()
    return joblib.load(path)

modelo_tiers = cargar_modelo_tiers()


def clasificar_jugador(user_data: dict):
    """
    Recibe datos de usuario y predice su Tier usando el modelo entrenado.
    """
    X = pd.DataFrame([{
        "nivel_experiencia": user_data.get("nivel_experiencia", 50),
        "consistencia": user_data.get("consistencia", 70),
        "tiempo_promedio": user_data.get("tiempo_promedio", 120),
        "diversificacion": user_data.get("diversificacion", 60)
    }])

    tier_predicho = modelo_tiers.predict(X)[0]

    return {
        "user_id": user_data.get("user_id", 0),
        "nombre": user_data.get("nombre", "Desconocido"),
        "nivel_experiencia": user_data.get("nivel_experiencia", 0),
        "tier_asignado": tier_predicho
    }
