# app/models/experience_level.py
from sqlalchemy import Column, Integer, Float, DateTime
from app.core.database import Base
from datetime import datetime


class ExperienceLevel(Base):
    __tablename__ = "experience_levels"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    score = Column(Integer, nullable=False)  # Nivel calculado [1-100]
    performance = Column(Float, nullable=False)
    consistency = Column(Float, nullable=False)
    diversification = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)