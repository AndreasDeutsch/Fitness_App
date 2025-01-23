from datetime import date
from pydantic import BaseModel
from typing import List

class Base(BaseModel):
    workout_spot_number = int
    workout_id = int
    spot_id = int


