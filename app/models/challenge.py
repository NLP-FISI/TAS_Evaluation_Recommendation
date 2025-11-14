# app/models/challenge.py
from sqlalchemy import Column, Integer, Float, Text, String
from app.core.database import Base

class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    internal_difficulty = Column(String(50), nullable=False)
    external_complexity_score = Column(
        Float, nullable=True)  # ← Nueva métrica RF4
    external_complexity_level = Column(String(50), nullable=True)