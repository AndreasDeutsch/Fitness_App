from typing import Generator

from database.config import async_session
from crud.user import UserCRUD
from crud.workout import WorkoutCRUD
from crud.exercise import ExerciseCRUD
from crud.set import SetCRUD
from crud.workout_spot import WorkoutSpotCRUD



async def get_db() -> Generator:
    async with async_session() as session:
        async with session.begin():
            yield session


async def get_user_crud() -> Generator:
    async with async_session() as session:
        async with session.begin():
            yield UserCRUD(session)

async def get_workout_crud() -> Generator:
    async with async_session() as session:
        async with session.begin():
            yield WorkoutCRUD(session)

async def get_exercise_crud() -> Generator:
    async with async_session() as session:
        async with session.begin():
            yield ExerciseCRUD(session)

async def get_set_crud() -> Generator:
    async with async_session() as session:
        async with session.begin():
            yield SetCRUD(session)

async def get_workout_spot_crud() -> Generator:
    async with async_session() as session:
        async with session.begin():
            yield WorkoutSpotCRUD(session)
