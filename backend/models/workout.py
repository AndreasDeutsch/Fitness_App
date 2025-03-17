from datetime import datetime

from sqlalchemy import Column, VARCHAR, DATE, DateTime, UniqueConstraint, INTEGER, ForeignKey
from sqlalchemy.orm import relationship
from database.config import Base



class WorkoutModels(Base):
    __tablename__ = "workouts"
    workout_id = Column(INTEGER, primary_key=True, autoincrement=True)
    start_datetime = Column(DateTime)
    end_datetime = Column(DateTime, nullable=True)
    name = Column(VARCHAR, nullable=False)
    user_id = Column(INTEGER, ForeignKey("users.user_id"))
    user = relationship("UserModels", back_populates="workouts")
    workout_exercises = relationship("ExerciseWorkoutModels", back_populates="workouts")
    
    def __init__(self, user_id: int, start_datetime: datetime, name = str):
        self.start_datetime = start_datetime
        self.user_id = user_id
        self.name = name

    def __repr__(self) -> str:
        return f"<WorkoutModels(date={self.start_datetime}, user_id={self.user_id})>"