# This module aggregates all API routes for version 1 of the API.
from fastapi import APIRouter
from . import evaluation_input
from . import profiling  # 1. Importar el nuevo módulo de profiling

router = APIRouter()
router.include_router(evaluation_input.router)
router.include_router(profiling.router) # 2. Incluir las nuevas rutas en el router principal
