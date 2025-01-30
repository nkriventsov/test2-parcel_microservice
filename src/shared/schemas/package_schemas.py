from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class PackageCreateRequest(BaseModel):
    name: str
    weight: float = Field(..., gt=0, description="Вес должен быть больше 0")
    type_id: int
    content_value: float = Field(..., ge=0, description="Стоимость содержимого не должна быть отрицательной")


class PackageCreate(PackageCreateRequest):
    id: int | None = Field(None, description="Идентификатор посылки")
    delivery_cost: float
    session_id: str


class PackageResponse(BaseModel):
    id: int
    name: str
    weight: float
    type_id: int
    # type_name: str
    content_value: float
    delivery_cost: Optional[float]

    model_config = ConfigDict(from_attributes=True)


class PackageUpdate(BaseModel):
    name: Optional[str]
    weight: Optional[float] = Field(None, gt=0, description="Вес должен быть больше 0")
    type_id: Optional[int]
    content_value: Optional[float] = Field(None, ge=0, description="Стоимость содержимого не должна быть отрицательной")
