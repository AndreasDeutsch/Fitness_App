from fastapi import APIRouter, Depends
from typing import List
import schemas.exercise as exercise
from sqlalchemy.ext.asyncio import AsyncSession

from crud.exercise import ExerciseCRUD
from crud.dependencies import get_exercise_crud
import schemas.exercise as exercise_schema

router = APIRouter(prefix="/exercises", tags=["exercises"])

@router.get("", response_model=List[exercise.Full])
async def get_exercises(skip: int = 0, limit: int = 10, db: ExerciseCRUD = Depends(get_exercise_crud)):
    return await db.get_exercises(skip=skip, limit=limit)


@router.get("/{exercise_id}", response_model=exercise.Full)	
async def get_exercise_by_id(exercise_id: int, db: ExerciseCRUD = Depends(get_exercise_crud)):
    return await db.get_exercise_by_id(exercise_id)

@router.post("")
async def create_exercise(new_exercise: exercise.Base, db: ExerciseCRUD = Depends(get_exercise_crud)):
    return await db.create_exercise(new_exercise)

@router.delete("/{exercise_id}")
async def delete_exercise(exercise_id: int, db: ExerciseCRUD = Depends(get_exercise_crud)):
    return await db.delete_exercise(exercise_id)

@router.put("/{exercise_id}")
async def update_exercise(exercise_id: int, new_exercise: exercise.Base, db: ExerciseCRUD = Depends(get_exercise_crud)):
    return await db.update_exercise(exercise_id, new_exercise)