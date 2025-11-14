# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import router as api_router

app = FastAPI(
    title="Recomendación y Evaluación API",
    description="Módulo del proyecto educativo gamificado - UNMSM",
    version="1.0.0"
)

# Permitir cualquier conexión (CORS abierto)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Permite todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],        # Permite todos los métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],        # Permite cualquier cabecera
)

# Rutas principales
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido a la API"}
# uvicorn app.main:app --reload
