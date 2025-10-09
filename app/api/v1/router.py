# This module aggregates all API routes for version 1 of the API.
from fastapi import APIRouter
from . import evaluation_input, evaluation_challenges
from .evaluation_analytics import router as evaluation_analytics_router


router = APIRouter()
router.include_router(evaluation_input.router)

router.include_router(evaluation_challenges.router)

router.include_router(evaluation_analytics_router)
