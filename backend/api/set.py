from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from crud.dependencies import get_set_crud

from crud.set import SetCRUD
import schemas.set as set_schema

router = APIRouter()

@router.get("/sets", response_model=List[set_schema.Base])
async def read_sets(skip: int = 0, limit: int = 10, db: SetCRUD = Depends(get_set_crud)):
    return await db.get_sets(skip=skip, limit=limit)

@router.get("/sets/{set_id}", response_model=set_schema.Base)
async def read_set(set_id: int):
    set = await SetCRUD().get_set_by_id(set_id)
    if set is None:
        raise HTTPException(status_code=404, detail="Set not found")
    return set

@router.post("/sets", response_model=set_schema.Base)
async def create_set(set: set_schema.Base):
    return await SetCRUD().create_set(set)

@router.delete("/sets/{set_id}", response_model=set_schema.Base)
async def delete_set(set_id: int):
    set = await SetCRUD().get_set_by_id(set_id)
    if set is None:
        raise HTTPException(status_code=404, detail="Set not found")
    await SetCRUD().delete_set(set_id)
    return set
