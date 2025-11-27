# app/services/recommendation_tipo_texto_service.py
from requests import Session
from sklearn.tree import DecisionTreeClassifier
import numpy as np

from app.models.tipo_texto import TipoTexto
from app.models.usuario import Usuario

modelo = None

def entrenar_modelo_tipo_texto():
    global modelo
    X = np.array([
        [8, 300, 0],    # edad, puntos, genero (0=M, 1=F)
        [12, 1200, 0],
        [15, 800, 1],
        [20, 500, 0],
        [10, 200, 1]
    ])
    y = np.array([
        "Narrativo",
        "Argumentativo",
        "Descriptivo",
        "Expositivo",
        "Dialogado"
    ])
    modelo = DecisionTreeClassifier()
    modelo.fit(X, y)
    return True

def recomendar_tipo_texto(usuario: Usuario, db: Session):
    global modelo

    entrada = np.array([[usuario.edad, usuario.puntos, 1 if usuario.genero == "F" else 0]])
    preferido = modelo.predict(entrada)[0]

    tipo = db.query(TipoTexto).filter(TipoTexto.nombre_tipo_texto == preferido).first()
    if not tipo:
        tipo = db.query(TipoTexto).order_by(TipoTexto.id_tipo_texto).first()

    return {
        "id_tipo_texto": tipo.id_tipo_texto,
        "nombre_tipo_texto": tipo.nombre_tipo_texto
    }

