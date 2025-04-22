from datetime import datetime

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from models.workout import WorkoutModels
import schemas.workout as workout_schema


class WorkoutCRUD:
    db_session = None

    def __init__(self, db_session: AsyncSession = None):
        self.db_session = db_session

    async def get_workout_by_id(self, workout_id: int):
        stmt = select(WorkoutModels).where(WorkoutModels.workout_id == workout_id)
        result = await self.db_session.execute(stmt)
        workout = result.scalars().first()
        return workout

    async def get_workouts(self, user_id: int, skip: int = 0, limit: int = 10) -> List[workout_schema.Base]:
        #stmt = select(WorkoutModels).offset(skip).limit(limit).join(WorkoutModels.workout_spots)
        stmt = select(WorkoutModels).where(WorkoutModels.user_id == user_id).offset(skip).limit(limit).order_by(WorkoutModels.start_datetime.desc())
        result = await self.db_session.execute(stmt)
        workouts = result.scalars().all()
        return workouts

    async def create_workout(self, workout: workout_schema.Base):
        db_workout = WorkoutModels(
            start_datetime=workout.start_datetime.replace(tzinfo=None),
            user_id=workout.user_id,
            name=workout.name
        )
        self.db_session.add(db_workout)
        await self.db_session.commit()
        return db_workout

    async def delete_workout(self, workout_id: int):
        stmt = delete(WorkoutModels).where(WorkoutModels.workout_id == workout_id)
        stmt.execution_options(synchronize_session="fetch")
        await self.db_session.execute(stmt)
        await self.db_session.commit()


    async def end_workout(self, workout_id: int, workout_end_datetime: datetime):
        workout = await self.get_workout_by_id(workout_id)
        if workout is None:
            return None
        stmt = update(WorkoutModels).where(WorkoutModels.workout_id == workout_id).values(end_datetime=workout_end_datetime.replace(tzinfo=None))
        stmt.execution_options(synchronize_session="fetch")
        await self.db_session.execute(stmt)
        new_workout = await self.get_workout_by_id(workout_id)
        await self.db_session.commit()
        return new_workout