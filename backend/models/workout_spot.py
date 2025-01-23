from datetime import datetime

from sqlalchemy import Column, VARCHAR, DATE, DateTime, UniqueConstraint, INTEGER
from sqlalchemy.orm import relationship
from database.config import Base


class WorkoutSpotModels(Base):
    __tablename__ = "workout_spots"
    workout_spot_number = Column(int, primary_key=True)
    workout_id = Column(INTEGER, primary_key=True, foreign_key=True)
    set_id = Column(INTEGER, foreign_key=True)
    workout = relationship("WorkoutModels", back_populates="workout_spots")
    
    def __init__(self, workout_spot_number: int, workout_id: int, set_id: int):
        self.workout_spot_number = workout_spot_number
        self.workout_id = workout_id
        self.set_id = set_id

    def __repr__(self) -> str:
        return f"<WorkoutSpotModels(workout_spot_number={self.workout_spot_number}, workout_id={self.workout_id}, set_id={self.set_id})>"
