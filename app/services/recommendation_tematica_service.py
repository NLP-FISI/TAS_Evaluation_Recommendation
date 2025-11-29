from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.models.tematica import Tematica
from sklearn.neighbors import NearestNeighbors
import numpy as np


def recomendar_tematica(user_id: int, db: Session):
    # Obtener usuarios que tengan al menos una temática en sus preferencias
    usuarios = db.query(Usuario).filter(Usuario.preferencias.any()).all()
    if not usuarios:
        return None

    # Crear matriz de características
    X = np.array([
        [
            u.edad or 0,
            u.puntos or 0,
            u.monedas or 0
        ]
        for u in usuarios
    ])

    # Entrenar modelo de similitud
    model = NearestNeighbors(n_neighbors=3, metric='euclidean')
    model.fit(X)

    # Obtener usuario objetivo
    usuario_actual = db.query(Usuario).filter(
        Usuario.id_usuario == user_id).first()

    if not usuario_actual:
        return None

    user_vector = np.array([[
        usuario_actual.edad or 0,
        usuario_actual.puntos or 0,
        usuario_actual.monedas or 0
    ]])

    # Encontrar los usuarios más similares (vecinos)
    distances, indices = model.kneighbors(user_vector)

    # Obtener temáticas desde preferencias de usuarios similares
    tematicas_ids = []

    for idx in indices[0]:
        usuario_similar = usuarios[idx]

        for tematica in usuario_similar.preferencias:
            tematicas_ids.append(tematica.id_tematica)

    if not tematicas_ids:
        return None

    # Seleccionar la temática más frecuente
    tematica_id = max(set(tematicas_ids), key=tematicas_ids.count)

    tematica = db.query(Tematica).filter(
        Tematica.id_tematica == tematica_id
    ).first()

    return tematica
