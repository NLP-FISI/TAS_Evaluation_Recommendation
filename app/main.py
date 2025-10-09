# Main application file
from fastapi import FastAPI
from app.api.v1.router import router as api_router

app = FastAPI(
    title="Recomendación y Evaluación API",
    description="Módulo del proyecto educativo gamificado - UNMSM",
    version="1.0.0"
)

# Rutas principales
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido a la API"}
