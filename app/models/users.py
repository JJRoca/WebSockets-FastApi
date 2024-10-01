from sqlmodel import SQLModel,Field,ForeignKey,Relationship
from pydantic import EmailStr
from datetime import datetime

#DATABASE MODEL
class User(SQLModel, table= True):
    id: int|None = Field(default=None,primary_key=True)
    full_name: str = Field(max_length=50, nullable=True)
    email: EmailStr =Field(max_length=50, unique= True, index=True)
    username:str = Field(max_length=50, unique=True, index=True)
    password: str = Field(max_length=150)
    available: bool= Field(default=True)
    created_at: datetime= Field(default_factory=datetime.now)
    
    logins: list["UserLogin"]= Relationship(back_populates="user")

class UserLogin(SQLModel, table= True):
    id: int|None= Field(default=None, primary_key=True)
    user_id: int= Field(foreign_key="user.id") 
    login_time: datetime = Field(default_factory=datetime.now)
    #bidireccional relation
    user: User= Relationship(back_populates="logins")    