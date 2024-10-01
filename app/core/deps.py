from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from collections.abc import Generator
from sqlmodel import Session
from app.core.database import engine
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="token")

def get_session()->Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

SessionDeps=Annotated[Session, Depends(get_session)]

TokenDeps=Annotated[str, Depends(oauth2_scheme)]