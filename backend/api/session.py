from fastapi import APIRouter
from typing import List
import schemas.exercise as exercise

from crud.exercise import ExerciseCRUD

router = APIRouter(prefix="/exercises", tags=["exercises"])

@router.get("", response_model=List[exercise.Base])
async def get_excercises():
    return await ExerciseCRUD().get_exercises()

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