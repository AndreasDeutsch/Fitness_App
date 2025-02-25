from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from auth.action import get_current_user
from crud.user import UserCRUD
from crud.dependencies import get_user_crud
import schemas.user as user_schema

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=List[user_schema.Full])
async def get_users(db: UserCRUD = Depends(get_user_crud)):
    return await db.get_users()


@router.post("")
async def register(
    new_user: user_schema.Register, db: UserCRUD = Depends(get_user_crud)
):
    await db.create_user(new_user)
    return status.HTTP_201_CREATED






