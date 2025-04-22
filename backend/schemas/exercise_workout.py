from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

class Create(BaseModel):
    exercise_id: int
    workout_id: int

class Full(Create):
    exercise_workout_id: int
    workout_spot_number: int
    sets: Optional[List] = None
    active_time: Optional[float] = None  # Changed to float for seconds
    start_time: Optional[str] = None    # Changed to string for ISO format
    end_time: Optional[str] = None      # Changed to string for ISO format