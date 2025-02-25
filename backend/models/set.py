from datetime import datetime

from sqlalchemy import Column, VARCHAR, DATE, DateTime, UniqueConstraint, INTEGER, FLOAT, ForeignKey
from sqlalchemy.orm import relationship
from database.config import Base

class SetModels(Base):
    __tablename__ = "sets"
    set_id = Column(INTEGER, primary_key=True, autoincrement=True)
    reps = Column(INTEGER)
    weight = Column(FLOAT)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    exercise_id = Column(INTEGER, ForeignKey("exercises.exercise_id"))
    exercise = relationship("ExerciseModels", back_populates="sets")
    workout_spots = relationship("WorkoutSpotModels", back_populates="set")
    
    def __init__(self, reps: int, weight: float, start_time: datetime, end_time: datetime, exercise_id: int):
        self.reps = reps
        self.weight = weight
        self.start_time = start_time
        self.end_time = end_time
        self.exercise_id = exercise_id

    def __repr__(self) -> str:
        return f"<SetModels(reps={self.reps}, weight={self.weight}, start_time={self.start_time}, end_time={self.end_time}, exercise_id={self.exercise_id})>"
