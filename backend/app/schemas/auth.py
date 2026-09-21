from pydantic import BaseModel
from datetime import datetime


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class Tokens(BaseModel):
    access_token: str
    refresh_token: str
