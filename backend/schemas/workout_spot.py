from datetime import date
from pydantic import BaseModel
from typing import List, Optional

class Base(BaseModel):
    workout_spot_number: int
    workout_id: int
    set_id: int

class DeleteWorkoutSpot(BaseModel):
    workout_spot_number: int
    workout_id: int

class UpdateWorkoutSpot(BaseModel):
    workout_spot_number: Optional[int] = None
    workout_id: Optional[int] = None
    set_id: Optional[int] = None


