# This module aggregates all API routes for version 1 of the API.
from fastapi import APIRouter
from . import evaluation_input
from . import profiling
# from . import evaluation_challenges  # Comentado temporalmente (usa SQLAlchemy)
# from .evaluation_analytics import router as evaluation_analytics_router  # Comentado temporalmente


# --- Creación del enrutador ---
router = APIRouter()
router.include_router(evaluation_input.router)
router.include_router(profiling.router)
# router.include_router(evaluation_challenges.router)  # Comentado temporalmente
# router.include_router(evaluation_analytics_router)  # Comentado temporalmente