from pydantic import BaseModel
from typing import TypeVar, Generic

T= TypeVar("T", bound=BaseModel)

class MetaData(BaseModel):
    total : int
    current_page: int
    per_page: int
    total_page: int
    previous_page: int|None
    next_page: int|None

class ResponseModel(BaseModel, Generic[T]):
    data: list[T]
    meta: MetaData