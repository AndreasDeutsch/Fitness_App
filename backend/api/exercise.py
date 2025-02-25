from fastapi import APIRouter, Depends
from typing import List
import schemas.exercise as exercise
from sqlalchemy.ext.asyncio import AsyncSession

from crud.exercise import ExerciseCRUD

from typing import Generator

from database.config import async_session


async def get_db() -> Generator:
    async with async_session() as session:
        async with session.begin():
            yield session

router = APIRouter(prefix="/exercises", tags=["exercises"])

@router.get("", response_model=List[exercise.Base])
async def get_exercises(db_session: AsyncSession = Depends(get_db)):
    return await ExerciseCRUD(db_session).get_exercises()


@router.get("/{exercise_id}", response_model=exercise.Full)	
async def get_exercise_by_id(exercise_id: int):
    return await ExerciseCRUD().get_exercise_by_id(exercise_id)

@router.post("")
async def create_exercise(new_exercise: exercise.Base):
    return await ExerciseCRUD().create_exercise(new_exercise)

@router.delete("/{exercise_id}")
async def delete_exercise(exercise_id: int):
    return await ExerciseCRUD().delete_exercise(exercise_id)

@router.put("/{exercise_id}")
async def update_exercise(exercise_id: int, new_exercise: exercise.Base):
    return await ExerciseCRUD().update_exercise(exercise_id, new_exercise)