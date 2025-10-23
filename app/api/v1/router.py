# This module aggregates all API routes for version 1 of the API.
from fastapi import APIRouter
from . import evaluation_input
from . import profiling
from . import evaluation_challenges
from .evaluation_analytics import router as evaluation_analytics_router
from . import diagnostic # 1. Importar el nuevo módulo de diagnostic
from . import recommendation_users # Asegúrate que este también esté importado si existe

# --- Creación del enrutador ---
router = APIRouter()
router.include_router(evaluation_input.router)
router.include_router(profiling.router)
router.include_router(evaluation_challenges.router)
router.include_router(evaluation_analytics_router)
router.include_router(diagnostic.router) # 2. Incluir las nuevas rutas de diagnóstico
router.include_router(recommendation_users.router) 

# (Puedes añadir otros routers aquí si es necesario)