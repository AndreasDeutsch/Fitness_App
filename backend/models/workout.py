from datetime import datetime

from sqlalchemy import Column, VARCHAR, DATE, DateTime, UniqueConstraint, INTEGER
from sqlalchemy.orm import relationship
from database.config import Base



class WorkoutModels(Base):
    __tablename__ = "workouts"
    workout_id = Column(INTEGER, primary_key=True, autoincrement=True)
    start_datetime = Column(DateTime)
    end_datetime = Column(DateTime)
    user_id = Column(INTEGER, foreign_key=True)
    user = relationship("UserModels", back_populates="workouts")
    workout_spots = relationship("WorkoutSpotModels", back_populates="workout")
    
    def __init__(self, date: datetime, user_id: int):
        self.date = date
        self.user_id = user_id

    def __repr__(self) -> str:
        return f"<WorkoutModels(date={self.date}, user_id={self.user_id})>"