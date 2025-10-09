# This module aggregates all API routes for version 1 of the API.
from fastapi import APIRouter
from . import evaluation_input
from . import recommendation_users

router = APIRouter()
router.include_router(evaluation_input.router)
router.include_router(recommendation_users.router,
                      prefix="/users", tags=["Users"])
