from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.models.tipo_texto import TipoTexto
# from app.models.diagnostic import TipoTexto
import random


def entrenar_modelo_tipo_texto():
    """
    Simula un modelo entrenado de recomendación de tipo de texto.
    (En producción, aquí cargarías tu modelo .pkl o TensorFlow)
    """
    print("📚 Modelo de recomendación de tipo de texto cargado correctamente.")
    return True


def recomendar_tipo_texto(usuario: Usuario, db: Session):
    """
    Retorna un tipo de texto recomendado (id + nombre) para el usuario dado.
    Se basa en sus características (edad, puntos, grado, etc.)
    """

    # Ejemplo: el modelo usa una lógica simple para demostrar estructura.
    # Puedes reemplazar esto con tu predicción real.
    if usuario.edad < 10:
        preferido = "Narrativo"
    elif usuario.puntos > 1000:
        preferido = "Argumentativo"
    elif usuario.genero == "F":
        preferido = "Descriptivo"
    else:
        # Elegimos aleatoriamente un tipo si no cumple condiciones específicas
        preferido = random.choice(
            ["Expositivo", "Informativo", "Dialogado", "Poético"])

    # Buscar el tipo en BD
    tipo = db.query(TipoTexto).filter(
        TipoTexto.nombre_tipo_texto == preferido).first()
    if not tipo:
        tipo = db.query(TipoTexto).order_by(TipoTexto.id_tipo_texto).first()

    return {
        "id_tipo_texto": tipo.id_tipo_texto,
        "nombre_tipo_texto": tipo.nombre_tipo_texto
    }
