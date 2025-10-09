# This module aggregates all API routes for version 1 of the API.
from fastapi import APIRouter

from . import evaluation_input, evaluation_challenges, recommendation_difficulty

router = APIRouter()
router.include_router(evaluation_input.router)
router.include_router(recommendation_difficulty.router)
router.include_router(evaluation_challenges.router)

