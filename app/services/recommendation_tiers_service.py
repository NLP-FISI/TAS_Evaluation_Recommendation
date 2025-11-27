# app/services/recommendation_tiers_service.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


def entrenar_y_clasificar(df_entrenamiento: pd.DataFrame, user_data: dict):
    """
    Entrena un modelo de clasificación de tiers con los datos reales o históricos,
    y predice el tier del usuario sin guardar el modelo en disco.
    """

    # --- Preparar datos de entrenamiento ---
    X = df_entrenamiento[["nivel_experiencia", "consistencia", "tiempo_promedio", "diversificacion"]]
    y = df_entrenamiento["tier"]

    # --- Entrenar modelo ---
    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)

    # --- Crear DataFrame del usuario a clasificar ---
    X_user = pd.DataFrame([{
        "nivel_experiencia": user_data.get("nivel_experiencia", 50),
        "consistencia": user_data.get("consistencia", 70),
        "tiempo_promedio": user_data.get("tiempo_promedio", 120),
        "diversificacion": user_data.get("diversificacion", 60)
    }])

    # --- Clasificar ---
    tier_predicho = model.predict(X_user)[0]

    # --- Devolver resultado ---
    return {
        "user_id": user_data.get("user_id", 0),
        "nombre": user_data.get("nombre", "Desconocido"),
        "nivel_experiencia": user_data.get("nivel_experiencia", 0),
        "consistencia": user_data.get("consistencia", 0),
        "tiempo_promedio": user_data.get("tiempo_promedio", 0),
        "diversificacion": user_data.get("diversificacion", 0),
        "tier_asignado": tier_predicho
    }
