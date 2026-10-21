from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class UOMMasterCreate(BaseModel):
    uom_code: str
    uom_name: str
    uom_category: str
    decimal_places: int = 0
    description: Optional[str] = None
    active: bool = True


class UOMMasterUpdate(BaseModel):
    model_config = ConfigDict(title="UOM - Master Update")

    uom_name: Optional[str] = None
    uom_category: Optional[str] = None
    decimal_places: Optional[int] = None
    description: Optional[str] = None
    active: Optional[bool] = None


class UOMStructure(BaseModel):
    model_config = ConfigDict(
        title="UOM - Master Response",
        from_attributes=True,
    )

    uom_id: int
    uom_code: str
    uom_name: str
    uom_category: str
    decimal_places: int
    description: Optional[str]
    active: bool
    created_by_id: int
    created_at: datetime
    modified_by_id: int
    modified_at: datetime


class UOMResponse(BaseModel):
    success: bool
    message: str
    data: UOMStructure


class UOMResponseList(BaseModel):
    success: bool
    message: str
    data: list[UOMStructure]
