# This module aggregates all API routes for version 1 of the API.
from fastapi import APIRouter
from . import evaluation_performance
from . import evaluation_input
from . import evaluation_input, recommendation_difficulty, text_recommendation
from . import profiling
from . import evaluation_challenges
from . import recommendation_tiers
from . import recommendation_users
#from . import diagnostic
from . import recommendation_users
from . import recommendation_difficulty
from . import generation_recommendation
from . import recommendation_tematica
from . import recommendation_tipo_texto
from .evaluation_analytics import router as evaluation_analytics_router


# --- Creación de enrutadores ---
router = APIRouter()
router.include_router(evaluation_input.router)
router.include_router(text_recommendation.router)
router.include_router(evaluation_performance.router)
router.include_router(profiling.router)
router.include_router(evaluation_challenges.router)
router.include_router(evaluation_analytics_router)
#router.include_router(diagnostic.router)
router.include_router(recommendation_users.router) 
router.include_router(recommendation_tiers.router)
router.include_router(recommendation_users.router)
router.include_router(recommendation_difficulty.router)
router.include_router(generation_recommendation.router)
router.include_router(recommendation_tematica.router)
router.include_router(recommendation_tipo_texto.router)
