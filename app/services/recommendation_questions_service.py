from sqlalchemy.orm import Session
from app.models.recommendation import Pregunta, Dificultad
from collections import Counter, defaultdict
import random

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

def diversificar_tipos_pregunta(preguntas, porcentaje_no_predominante=0.3):
    # Contar tipos de pregunta
    tipos = [p.ID_TipoPregunta for p in preguntas]
    conteo = Counter(tipos)
    if not conteo:
        return []
    
    tipo_predominante = conteo.most_common(1)[0][0]
    preguntas_por_tipo = defaultdict(list)
    for p in preguntas:
        preguntas_por_tipo[p.ID_TipoPregunta].append(p)

    total = len(preguntas)
    min_no_predominante = max(1, int(total * porcentaje_no_predominante))

    # Seleccionar preguntas de tipos no predominantes
    seleccionadas = []
    restantes = []
    for tipo, lista in preguntas_por_tipo.items():
        if tipo != tipo_predominante:
            seleccionadas.extend(lista[:min_no_predominante])
            restantes.extend(lista[min_no_predominante:])
        else:
            restantes.extend(lista)

    # Completar con preguntas del tipo predominante hasta el límite original
    faltantes = total - len(seleccionadas)
    seleccionadas.extend(restantes[:faltantes])

    # Mezclar para evitar agrupamiento por tipo
    random.shuffle(seleccionadas)
    return seleccionadas