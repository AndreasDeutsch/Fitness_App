from datetime import datetime

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from models.workout_spot import WorkoutSpotModels
import schemas.workout_spot as workout_spot_schema


class WorkoutSpotCRUD():
    db_session = None

    def __init__(self, db_session: AsyncSession = None):
        self.db_session = db_session

    async def get_workout_spots_for_workout(self, workout_id: int) -> List[workout_spot_schema.Base]:
        stmt = select(WorkoutSpotModels).where(WorkoutSpotModels.workout_id == workout_id)
        result = await self.db_session.execute(stmt)
        workout_spots = result.scalars().first()
        return workout_spots

    async def create_workout_spot(self, workout_spot: workout_spot_schema.Base) -> workout_spot_schema.Base:
        db_workout_spot = WorkoutSpotModels(
            workout_spot_number=workout_spot.workout_spot_number,
            workout_id=workout_spot.workout_id,
            set_id=workout_spot.set_id
        )
        self.db_session.add(db_workout_spot)
        await self.db_session.commit()
        return db_workout_spot

    async def delete_workout_spot(self, delete_workout_spot: workout_spot_schema.DeleteWorkoutSpot):
        stmt = delete(WorkoutSpotModels).where(WorkoutSpotModels.workout_id == delete_workout_spot.workout_id).where(WorkoutSpotModels.workout_spot_number == delete_workout_spot.workout_spot_number)
        stmt.execution_options(synchronize_session="fetch")
        await self.db_session.execute(stmt)

    async def update_workout_spot(self, workout_spot: workout_spot_schema.UpdateWorkoutSpot) -> workout_spot_schema.Base:
        stmt = update(WorkoutSpotModels).where(
            WorkoutSpotModels.workout_id == workout_spot.workout_id,
            WorkoutSpotModels.workout_spot_number == workout_spot.workout_spot_number
        ).values(
            set_id=workout_spot.set_id
        ).execution_options(synchronize_session="fetch")
        await self.db_session.execute(stmt)
        await self.db_session.commit()
        return await self.get_workout_spot_by_id(workout_spot.workout_id, workout_spot.workout_spot_number)

    async def get_workout_spot_by_id(self, workout_id: int, workout_spot_number: int) -> workout_spot_schema.Base:
        stmt = select(WorkoutSpotModels).where(
            WorkoutSpotModels.workout_id == workout_id,
            WorkoutSpotModels.workout_spot_number == workout_spot_number
        )
        result = await self.db_session.execute(stmt)
        workout_spot = result.scalars().first()
        return workout_spot
