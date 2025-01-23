from datetime import datetime

from sqlalchemy import Column, VARCHAR, DATE, DateTime, UniqueConstraint, INTEGER
from sqlalchemy.orm import relationship
from database.config import Base


class ExerciseModels(Base):
    __tablename__ = "exercises"
    exercise_id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(VARCHAR)
    user_id = Column(INTEGER, foreign_key=True)
    user = relationship("UserModels", back_populates="exercises")
    sets = relationship("SetModels", back_populates="exercise")
    
    def __init__(self, name: str, user_id: int):
        self.name = name
        self.user_id = user_id

    def __repr__(self) -> str:
        return f"<ExerciseModels(name={self.name}, user_id={self.user_id})>"
    