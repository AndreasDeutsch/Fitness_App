from datetime import datetime

from sqlalchemy import Column, VARCHAR, DATE, DateTime, UniqueConstraint, INTEGER
from sqlalchemy.orm import relationship
from database.config import Base


class UserModels(Base):
    __tablename__ = "users"
    user_id = Column(INTEGER, primary_key=True, autoincrement=True)
    firstname = Column(VARCHAR)
    lastname = Column(VARCHAR)
    email = Column(VARCHAR, unique=True)
    password_hash = Column(VARCHAR)
    exercises = relationship("ExerciseModels", back_populates="user")
    workouts = relationship("WorkoutModels", back_populates="user")
    
    def __init__(self, firstname: str, lastname: str, email: str, password_hash: str):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password_hash = password_hash

    def __repr__(self) -> str:
        return f"<UserModels(fistname={self.firstname}, lastname={self.lastname}, email={self.email})>"
    

