import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# --- Modelo de Tiers (usando entrenamiento previo) ---


def entrenar_modelo_tiers(df_entrenamiento):
    """
    Entrena un modelo con datos reales o históricos.
    """
    X = df_entrenamiento[["nivel_experiencia",
                          "consistencia", "tiempo_promedio", "diversificacion"]]
    y = df_entrenamiento["tier"]

    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)

    os.makedirs("app/fake_model", exist_ok=True)
    joblib.dump(model, "app/fake_model/tiers_model.pkl")
    return model


def cargar_modelo_tiers():
    """
    Carga el modelo ya entrenado o lanza error si no existe.
    """
    path = "app/fake_model/tiers_model.pkl"
    if not os.path.exists(path):
        raise FileNotFoundError(
            "El modelo de clasificación de tiers no existe. Entrénalo primero.")
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
        "consistencia": user_data.get("consistencia", 0),
        "tiempo_promedio": user_data.get("tiempo_promedio", 0),
        "diversificacion": user_data.get("diversificacion", 0),
        "tier_asignado": tier_predicho
    }
