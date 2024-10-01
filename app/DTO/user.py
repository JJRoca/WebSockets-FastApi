from pydantic import BaseModel,Field,EmailStr
from datetime import datetime
class UserBase(BaseModel):
    full_name: str|None = Field(max_length=150)
    email: EmailStr
    username: str = Field(min_length=3, max_length=30)

class UserCreate(UserBase):
    password: str

class UserPublic(UserBase):
    id: int
    available: bool
    created_at: datetime


class UserUpdate(BaseModel):
    id: int|None= None
    full_name: str|None= None
    email: EmailStr|None= None
    username: str|None= None


class UserUpdatePassword(BaseModel):
    current_password: str = Field(min_length=8,max_length=50)
    new_password: str = Field(min_length=8,max_length=50)


