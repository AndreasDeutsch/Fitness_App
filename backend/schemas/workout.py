from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class Base(BaseModel):
    start_datetime: datetime
    user_id: int
    name: str

class WorkoutCreate(Base):
    pass

class Workout(Base):
    workout_id: int

    class Config:
        orm_mode: True


class Full(Base):
    end_datetime: Optional[datetime]

    class Config:
        orm_mode: True