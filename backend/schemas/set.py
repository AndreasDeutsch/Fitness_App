from datetime import datetime
from pydantic import BaseModel
from typing import List

class Base(BaseModel):
    reps = int
    weight = float
    start_time = datetime
    end_time = datetime
    exercise_id = int

class Full(Base):
    set_id = int

