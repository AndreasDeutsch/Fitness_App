from fastapi import APIRouter, Depends
from typing import List
import schemas.exercise_workout as exercise_workout_schema
from sqlalchemy.ext.asyncio import AsyncSession

from crud.exercise_workout import ExerciseWorkoutCRUD
from crud.dependencies import get_exercise_workout_crud

router = APIRouter(prefix="/exercise_workouts", tags=["exercise_workouts"])

@router.post("", response_model=exercise_workout_schema.Full)
async def create_exercise_workout(new_exercise_workout: exercise_workout_schema.Create, db: ExerciseWorkoutCRUD = Depends(get_exercise_workout_crud)):
    return await db.create_exercise_workout(new_exercise_workout)

@router.get("/{exercise_workout_id}", response_model=exercise_workout_schema.Full)
async def get_exercise_workout_by_id(exercise_workout_id: int, db: ExerciseWorkoutCRUD = Depends(get_exercise_workout_crud)):
    return await db.get_exercise_workout_by_id(exercise_workout_id)

@router.get("/workout/{workout_id}", response_model=List[exercise_workout_schema.Full])
async def get_exercise_workouts_for_workout(workout_id: int, skip: int = 0, limit: int = 100, db: ExerciseWorkoutCRUD = Depends(get_exercise_workout_crud)):
    return await db.get_exercise_workouts_for_workout(workout_id, skip, limit)

@router.delete("/{exercise_workout_id}")
async def delete_exercise_workout(exercise_workout_id: int, db: ExerciseWorkoutCRUD = Depends(get_exercise_workout_crud)):
    return await db.delete_exercise_workout(exercise_workout_id)
