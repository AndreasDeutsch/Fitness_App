from datetime import datetime

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
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
        print(db_exercise_workout.to_dict())
        return db_exercise_workout.to_dict()

    
    async def get_exercise_workout_by_id(self, exercise_workout_id: int) -> exercise_workout_schema.Full:
        stmt = select(ExerciseWorkoutModels).where(ExerciseWorkoutModels.exercise_workout_id == exercise_workout_id).options(joinedload(ExerciseWorkoutModels.sets))
        result = await self.db_session.execute(stmt)
        exercise_workout = result.scalars().first()
        if exercise_workout:
            exercise_workout_dict = exercise_workout.to_dict()
            exercise_workout_dict['sets'] = [set.to_dict() for set in exercise_workout.sets]
            return exercise_workout_dict
        return None
    
    async def get_exercise_workouts_for_workout(self, workout_id, skip, limit) -> List[exercise_workout_schema.Full]:
        stmt = select(ExerciseWorkoutModels).where(ExerciseWorkoutModels.workout_id == workout_id).options(joinedload(ExerciseWorkoutModels.sets)).offset(skip).limit(limit)
        result = await self.db_session.execute(stmt)
        exercise_workouts = result.unique().scalars().all()
        exercise_workouts_dicts = []
        for exercise_workout in exercise_workouts:
            exercise_workout_dict = exercise_workout.to_dict()
            exercise_workout_dict['sets'] = [set.to_dict() for set in exercise_workout.sets]
            exercise_workouts_dicts.append(exercise_workout_dict)
        return exercise_workouts_dicts

    async def delete_exercise_workout(self, exercise_workout_id: int) -> exercise_workout_schema.Full:
        exercise_workout = await self.get_exercise_workout_by_id(exercise_workout_id)
        if not exercise_workout:
            return None
        
        stmt = delete(ExerciseWorkoutModels).where(ExerciseWorkoutModels.exercise_workout_id == exercise_workout_id)
        await self.db_session.execute(stmt)
        await self.db_session.commit()
        
        return exercise_workout
