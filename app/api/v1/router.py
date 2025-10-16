# This module aggregates all API routes for version 1 of the API.
from fastapi import APIRouter
from . import evaluation_input
from . import profiling
from . import evaluation_challenges
from . import recommendation_tiers
from . import recommendation_users
from .evaluation_analytics import router as evaluation_analytics_router


# --- Creación del enrutador ---
router = APIRouter()
router.include_router(evaluation_input.router)
router.include_router(profiling.router)
router.include_router(evaluation_challenges.router)
router.include_router(evaluation_analytics_router)
router.include_router(recommendation_tiers.router)
router.include_router(recommendation_users.router)
