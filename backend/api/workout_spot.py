from fastapi import APIRouter, Depends
from typing import List
import schemas.workout_spot as workout_spot
from crud.workout_spot import WorkoutSpotCRUD
from crud.dependencies import get_workout_spot_crud

router = APIRouter(prefix="/workout_spots", tags=["workout_spots"])

@router.get("/{workout_id}", response_model=List[workout_spot.Base])
async def get_workout_spots_for_workout(workout_id: int, db: WorkoutSpotCRUD = Depends(get_workout_spot_crud)):
    return await db.get_workout_spots_for_workout(workout_id)

@router.post("")
async def create_workout_spot(new_workout_spot: workout_spot.Base, db: WorkoutSpotCRUD = Depends(get_workout_spot_crud)):
    return await db.create_workout_spot(new_workout_spot)

@router.delete("/{workout_id}/{workout_spot_number}")
async def delete_workout_spot(workout_id: int, workout_spot_number: int, db: WorkoutSpotCRUD = Depends(get_workout_spot_crud)):
    return await db.delete_workout_spot(workout_id, workout_spot_number)

@router.put("/{workout_id}/{workout_spot_number}")
async def update_workout_spot(workout_id: int, workout_spot_number: int, new_workout_spot: workout_spot.Base, db: WorkoutSpotCRUD = Depends(get_workout_spot_crud)):
    return await db.update_workout_spot(workout_id, workout_spot_number, new_workout_spot)

@router.get("/{workout_id}/{set_id}", response_model=List[workout_spot.Base])
async def get_workout_spots_for_set(workout_id: int, set_id: int, db: WorkoutSpotCRUD = Depends(get_workout_spot_crud)):
    return await db.get_workout_spots_for_set(workout_id, set_id)
