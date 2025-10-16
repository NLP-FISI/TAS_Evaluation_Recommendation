# app/services/jobs.py
from app.services.recommendation_users_service import calculate_experience_level


def recalculate_experience_batch(user_ids: list[int]):
    for user_id in user_ids:
        # TODO: traer métricas históricas reales de DB
        performance, consistency, diversification = 70, 65, 55
        calculate_experience_level(
            user_id, performance, consistency, diversification)
