from pydantic import BaseModel
from typing import Optional


class TypeCreate(BaseModel):
    name: str


class TypeResponse(TypeCreate):
    id: int


class TypeUpdate(BaseModel):
    name: Optional[str]