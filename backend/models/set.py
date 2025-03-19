from datetime import datetime

from sqlalchemy import Column, VARCHAR, DATE, DateTime, UniqueConstraint, INTEGER, FLOAT, ForeignKey
from sqlalchemy.orm import relationship
from database.config import Base

class SetModels(Base):
    __tablename__ = "sets"
    set_id = Column(INTEGER, primary_key=True, autoincrement=True)
    reps = Column(INTEGER, nullable=True)
    weight = Column(FLOAT, nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    exercise_workout_id = Column(INTEGER, ForeignKey("exercise_workout.exercise_workout_id"), nullable=False)
    exercise_workouts = relationship("ExerciseWorkoutModels", back_populates="sets")
    
    def __init__(self, start_time: datetime, exercise_workout_id: int):
        self.start_time = start_time
        self.exercise_workout_id = exercise_workout_id

        
    def __repr__(self) -> str:
        return f"<SetModels(reps={self.reps}, weight={self.weight}, start_time={self.start_time}, end_time={self.end_time}, exercise_id={self.exercise_id})>"


    def to_dict(self):
        return {
            "set_id": self.set_id,
            "reps": self.reps,
            "weight": self.weight,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "exercise_workout_id": self.exercise_workout_id
        }
    
    def to_dict_create_return(self):
        return {
            "set_id": self.set_id,
            "start_time": self.start_time,
            "exercise_workout_id": self.exercise_workout_id
        }