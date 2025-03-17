from datetime import datetime

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from auth.utils import get_password_hash
from models.exercise import ExerciseModels
import schemas.exercise as exercise_schema

class ExerciseCRUD():
    db_session = None

    def __init__(self, db_session: AsyncSession = None):
        self.db_session = db_session


    async def get_exercises(self, skip, limit) -> List[exercise_schema.Base]:
        stmt = select(ExerciseModels).offset(skip).limit(limit)
        result = await self.db_session.execute(stmt)
        exercises = result.scalars().all()
        return exercises        
    
    async def get_exercise_by_id(self, exercise_id: int) -> exercise_schema.Full:
        stmt = select(ExerciseModels).where(ExerciseModels.exercise_id == exercise_id)
        result = await self.db_session.execute(stmt)
        exercise = result.scalars().all()
        return exercise
    
    async def create_exercise(self, exercise: exercise_schema.Base) -> exercise_schema.Base:
        db_exercise = ExerciseModels(
            name=exercise.name,
            user_id=exercise.user_id
        )
        self.db_session.add(db_exercise)
        await self.db_session.commit()
        return db_exercise


    async def delete_exercise(self, exercise_id: int):
        stmt = delete(ExerciseModels).where(ExerciseModels.exercise_id == exercise_id)
        stmt.execution_options(synchronize_session="fetch")
        await self.db_session.execute(stmt)