# This module aggregates all API routes for version 1 of the API.
from fastapi import APIRouter
from . import evaluation_input

router = APIRouter()
router.include_router(evaluation_input.router)
