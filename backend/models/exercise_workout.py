from datetime import datetime

from sqlalchemy import Column, VARCHAR, DATE, DateTime, UniqueConstraint, INTEGER, ForeignKey
from sqlalchemy.orm import relationship
from database.config import Base


class ExerciseWorkoutModels(Base):
    __tablename__ = "exercise_workout"
    exercise_workout_id = Column(INTEGER, primary_key=True, autoincrement=True)
    workout_spot_number = Column(INTEGER, nullable=False)
    workout_id = Column(INTEGER, ForeignKey("workouts.workout_id"), nullable=False)
    exercise_id = Column(INTEGER, ForeignKey("exercises.exercise_id"), nullable=False)
    
    __table_args__ = (UniqueConstraint('workout_spot_number', 'workout_id', name='_workout_spot_workout_uc'),)
    
    workouts = relationship("WorkoutModels", back_populates="workout_exercises")
    exercise = relationship("ExerciseModels", back_populates="exercise_workouts")
    sets = relationship("SetModels", back_populates="exercise_workouts")
    
    def __init__(self, exercise_id: int, workout_id: int, workout_spot_number: int):
        self.exercise_id = exercise_id
        self.workout_id = workout_id
        self.workout_spot_number = workout_spot_number