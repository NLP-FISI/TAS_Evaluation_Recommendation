from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.models.tematica import Tematica
from sklearn.neighbors import NearestNeighbors
import numpy as np


def recomendar_tematica(user_id: int, db: Session):
    # Obtener todos los usuarios y sus temáticas
    usuarios = db.query(Usuario).filter(Usuario.id_tematica.isnot(None)).all()
    if not usuarios:
        return None

    # Crear matriz de características
    X = np.array([[u.edad or 0, u.puntos or 0, u.monedas or 0]
                 for u in usuarios])

    # Entrenar modelo de similitud
    model = NearestNeighbors(n_neighbors=3, metric='euclidean')
    model.fit(X)

    # Obtener usuario objetivo
    usuario_actual = db.query(Usuario).filter(
        Usuario.id_usuario == user_id).first()
    if not usuario_actual:
        return None

    user_vector = np.array(
        [[usuario_actual.edad or 0, usuario_actual.puntos or 0, usuario_actual.monedas or 0]])

    # Encontrar los usuarios más similares
    distances, indices = model.kneighbors(user_vector)

    # Recolectar las temáticas más frecuentes entre los similares
    tematicas_ids = [usuarios[i].id_tematica for i in indices[0]
                     if usuarios[i].id_tematica]
    if not tematicas_ids:
        return None

    # Tomar la temática más repetida o la primera si hay empate
    tematica_id = max(set(tematicas_ids), key=tematicas_ids.count)

    tematica = db.query(Tematica).filter(
        Tematica.id_tematica == tematica_id).first()
    return tematica
