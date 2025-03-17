from datetime import datetime
from pydantic import BaseModel
from typing import List

class Base(BaseModel):
    start_time: datetime
    exercise_workout_id: int

class CreateReturn(Base):
    set_id: int

class Finish(BaseModel):
    set_id: int
    reps: int
    weight: float
    end_time: datetime

class Full(CreateReturn):
    reps: int
    weight: float
    end_time: datetime

