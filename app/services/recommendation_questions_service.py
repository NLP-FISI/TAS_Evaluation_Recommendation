from sqlalchemy.orm import Session
from app.models.recommendation import Pregunta, Dificultad

def filtrar_preguntas_por_dificultad(db: Session, dificultad_recomendada: int, limite: int = 10):
    # Busca el ID de dificultad más cercano si no existe una coincidencia exacta
    dificultad = db.query(Dificultad).filter(Dificultad.Valor_Dificultad ==dificultad_recomendada).first()
    if not dificultad:
        dificultad = db.query(Dificultad).order_by(
            abs(Dificultad.Valor_Dificultad - dificultad_recomendada)
        ).first()
    if not dificultad:
        return []
    
    preguntas = db.query(Pregunta).filter(Pregunta.ID_Dificultad == dificultad.ID_Dificultad).limit(limite).all()
    return preguntas