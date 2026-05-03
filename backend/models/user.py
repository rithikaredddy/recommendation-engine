from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    token: str

class RatingCreate(BaseModel):
    rating: float = Field(..., ge=1, le=5)
