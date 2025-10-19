from typing import List

_TEMPLATES = {
    "literal":     "Error de comprensión literal. Pistas: {pistas}. Grado {grado}.",
    "inferencial": "Error de comprensión inferencial. Pistas: {pistas}. Grado {grado}.",
    "critico":     "Error de comprensión crítica. Pistas: {pistas}. Grado {grado}.",
    "vocabulario": "Dificultad de vocabulario. Palabras: {pistas}. Grado {grado}.",
    "tiempo":      "Gestión de tiempo insuficiente. Claves: {pistas}. Grado {grado}.",
}

def build_error_text(tipo_error: str, grado: int, pistas: List[str] | None) -> str:
    tpl = _TEMPLATES.get(tipo_error, "Error de tipo {tipo}. Pistas: {pistas}. Grado {grado}.")
    pistas_str = ", ".join(pistas or [])
    return tpl.format(pistas=pistas_str, grado=grado, tipo=tipo_error)
