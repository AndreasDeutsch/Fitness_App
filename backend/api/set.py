from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from crud.dependencies import get_set_crud

from crud.set import SetCRUD
import schemas.set as set_schema

router = APIRouter(prefix="/set", tags=["set"])

@router.get("", response_model=List[set_schema.Full])
async def read_sets(skip: int = 0, limit: int = 10, db: SetCRUD = Depends(get_set_crud)):
    return await db.get_sets(skip=skip, limit=limit)

@router.get("/{set_id}", response_model=set_schema.Full)
async def read_set(set_id: int, db: SetCRUD = Depends(get_set_crud)):
    set = await db.get_set_by_id(set_id)
    if set is None:
        raise HTTPException(status_code=404, detail="Set not found")
    return set

@router.post("", response_model=set_schema.CreateReturn)
async def create_set(set: set_schema.Base, db: SetCRUD = Depends(get_set_crud)):
    return await db.create_set(set)

@router.post("/finish/", response_model=set_schema.Full)
async def create_set(set: set_schema.Finish, db: SetCRUD = Depends(get_set_crud)):
    return await db.finish_set(set)

@router.delete("/{set_id}", response_model=set_schema.Full)
async def delete_set(set_id: int, db: SetCRUD = Depends(get_set_crud)):
    set = await db.get_set_by_id(set_id)
    if set is None:
        raise HTTPException(status_code=404, detail="Set not found")
    await db.delete_set(set_id)
    return set
