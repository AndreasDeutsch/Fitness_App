from datetime import date
from pydantic import BaseModel
from typing import List

class Base(BaseModel):
    name = str
    user_id = int

class Full(Base):
    exercise_id = int

