# app/models/recommendation.py
from sqlalchemy import Column, Integer, Float, DateTime, Text, String
from sqlalchemy.orm import relationship
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


class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    internal_difficulty = Column(String(50), nullable=False)
    external_complexity_score = Column(
        Float, nullable=True)  # ← Nueva métrica RF4
    external_complexity_level = Column(String(50), nullable=True)
