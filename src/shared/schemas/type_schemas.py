from pydantic import BaseModel, ConfigDict
from typing import Optional


class TypeCreate(BaseModel):
    name: str


class TypeResponse(TypeCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TypeUpdate(BaseModel):
    name: Optional[str]