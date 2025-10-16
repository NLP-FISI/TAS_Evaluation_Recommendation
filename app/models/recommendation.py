# app/models/recommendation.py
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
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

class Dificultad(Base):
    __tablename__ = "Dificultad"
    ID_Dificultad = Column(Integer, primary_key=True)
    Nombre_Dificultad = Column(String(50))
    Valor_Dificultad = Column(Integer)

class Pregunta(Base):
    __tablename__ = "Pregunta"
    ID_Pregunta = Column(Integer, primary_key=True, index=True)
    ID_Texto = Column(Integer, ForeignKey("Texto.ID_Texto"))
    ID_TipoPregunta = Column(Integer, ForeignKey("Tipo_Pregunta.ID_Tipo_Pregunta"))
    ID_Dificultad = Column(Integer, ForeignKey("Dificultad.ID_Dificultad"))
    Contenido = Column(String(100))

    dificultad = relationship("Dificultad")