# This module aggregates all API routes for version 1 of the API.
from fastapi import APIRouter
from . import evaluation_input
from . import evaluation_input, recommendation_difficulty, text_recommendation

router = APIRouter()
router.include_router(evaluation_input.router)
router.include_router(text_recommendation.router)
