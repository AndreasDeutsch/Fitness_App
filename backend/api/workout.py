from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from crud.workout import WorkoutCRUD
from crud.dependencies import get_workout_crud
import schemas.workout as workout_schema

router = APIRouter(prefix="/workout", tags=["workout"])

@router.get("", response_model=List[workout_schema.Workout])
async def read_workouts(skip: int = 0, limit: int = 10, db: WorkoutCRUD = Depends(get_workout_crud)):
    return await db.get_workouts(skip=skip, limit=limit)

@router.get("/{workout_id}", response_model=workout_schema.Workout)
async def read_workout(workout_id: int, db: WorkoutCRUD = Depends(get_workout_crud)):
    workout = await db.get_workout_by_id(workout_id)
    if workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout

@router.post("", response_model=workout_schema.Workout)
async def create_workout(workout: workout_schema.Base, db: WorkoutCRUD = Depends(get_workout_crud)):
    return await db.create_workout(workout)

@router.delete("/{workout_id}", response_model=workout_schema.Workout)
async def delete_workout(workout_id: int, db: WorkoutCRUD = Depends(get_workout_crud)):
    workout = await db.get_workout_by_id(workout_id)
    if workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")
    await db.delete_workout(workout_id)
    return workout
