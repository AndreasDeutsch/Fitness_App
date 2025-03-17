from datetime import datetime

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from auth.utils import get_password_hash
from models.exercise_workout import ExerciseWorkoutModels
import schemas.exercise_workout as exercise_workout_schema

class ExerciseWorkoutCRUD():
    db_session = None

    def __init__(self, db_session: AsyncSession = None):
        self.db_session = db_session


    async def create_exercise_workout(self, exercise_workout: exercise_workout_schema.Create) -> exercise_workout_schema.Full:
        stmt = select(ExerciseWorkoutModels.workout_spot_number).where(ExerciseWorkoutModels.workout_id == exercise_workout.workout_id).order_by(ExerciseWorkoutModels.workout_spot_number.desc())
        result = await self.db_session.execute(stmt)
        last_spot_number = result.scalars().first()
        next_spot_number = (last_spot_number + 1) if last_spot_number is not None else 1

        db_exercise_workout = ExerciseWorkoutModels(
            exercise_id=exercise_workout.exercise_id,
            workout_id=exercise_workout.workout_id,
            workout_spot_number=next_spot_number
        )
        self.db_session.add(db_exercise_workout)
        await self.db_session.commit()
        await self.db_session.refresh(db_exercise_workout)
        return db_exercise_workout

    
    async def get_exercise_workout_by_id(self, exercise_workout_id: int) -> exercise_workout_schema.Full:
        stmt = select(ExerciseWorkoutModels).where(ExerciseWorkoutModels.exercise_workout_id == exercise_workout_id)
        result = await self.db_session.execute(stmt)
        exercise_workout = result.scalars().first()
        return exercise_workout
    
    async def get_exercise_workouts_for_workout(self, workout_id, skip, limit) -> List[exercise_workout_schema.Full]:
        stmt = select(ExerciseWorkoutModels).where(ExerciseWorkoutModels.workout_id == workout_id).offset(skip).limit(limit)
        result = await self.db_session.execute(stmt)
        exercise_workouts = result.scalars().all()
        for exercise_workout in exercise_workouts:
            await self.db_session.refresh(exercise_workout)
        return exercise_workouts

    async def delete_exercise_workout(self, exercise_workout_id: int) -> exercise_workout_schema.Full:
        stmt = delete(ExerciseWorkoutModels).where(ExerciseWorkoutModels.exercise_workout_id == exercise_workout_id)
        result = await self.db_session.execute(stmt)
        return result
