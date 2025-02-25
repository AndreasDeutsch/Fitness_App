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
    
    async def get_sets(self, skip: int = 0, limit: int = 10) -> List[set_schema.Base]:
        stmt = select(SetModels)
        result = await self.db_session.execute(stmt)
        sets = result.scalars().all()
        return sets
    
    async def create_set(self, set: set_schema.Base):
        db_set = SetModels(
            reps=set.reps,
            weight=set.weight,
            start_time=set.start_time,
            end_time=set.end_time,
            exercise_id=set.exercise_id
        )
        self.db_session.add(db_set)
        await self.db_session.commit()
        return db_set
    
    async def delete_set(self, set_id: int):
        stmt = delete(SetModels).where(SetModels.set_id == set_id)
        stmt.execution_options(synchronize_session="fetch")
        await self.db_session.execute(stmt)
