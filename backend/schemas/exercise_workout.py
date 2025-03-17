from datetime import datetime
from pydantic import BaseModel
from typing import List

class Create(BaseModel):
    exercise_id: int
    workout_id: int

class Full(Create):
    exercise_workout_id: int
    workout_spot_number: int
    sets: List