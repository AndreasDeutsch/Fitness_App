from datetime import datetime

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from auth.utils import get_password_hash
from models.set import SetModels
import schemas.set as set_schema


class SetCRUD:
    db_session = None

    def __init__(self, db_session: AsyncSession = None):
        self.db_session = db_session


    async def get_set_by_id(self, set_id):
        stmt = select(SetModels).where(SetModels.set_id == set_id)
        result = await self.db_session.execute(stmt)
        set = result.scalars().first()
        return set
    
    async def get_sets(self, skip: int = 0, limit: int = 10) -> List[set_schema.Full]:
        stmt = select(SetModels)
        result = await self.db_session.execute(stmt)
        sets = result.scalars().all()
        return sets
    
    async def create_set(self, set: set_schema.Base) -> set_schema.CreateReturn:
        db_set = SetModels(
            start_time=set.start_time.replace(tzinfo=None),
            exercise_workout_id=set.exercise_workout_id
        )
        self.db_session.add(db_set)
        await self.db_session.commit()
        await self.db_session.refresh(db_set)
        return db_set

    async def finish_set(self, data: set_schema.Finish) -> set_schema.Full:
        stmt = update(SetModels).where(SetModels.set_id == data.set_id).values(
            end_time=data.end_time.replace(tzinfo=None),
            reps=data.reps,
            weight=data.weight
        )
        await self.db_session.execute(stmt)
        await self.db_session.commit()
        stmt = select(SetModels).where(SetModels.set_id == data.set_id)
        result = await self.db_session.execute(stmt)
        updated_set = result.scalars().first()
        return updated_set

    async def delete_set(self, set_id: int):
        stmt = delete(SetModels).where(SetModels.set_id == set_id)
        stmt.execution_options(synchronize_session="fetch")
        await self.db_session.execute(stmt)
