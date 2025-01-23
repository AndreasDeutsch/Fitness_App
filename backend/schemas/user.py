from datetime import date

from pydantic import BaseModel

from typing import List
# User Schema


class Base(BaseModel):
    firstname: str
    lastname: str
    email: str

class Register(Base):
    password_hash: str

class Password(BaseModel):
    password: str

class Full(Base):
    user_id: int


