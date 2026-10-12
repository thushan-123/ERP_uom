from datetime import datetime
from typing import Optional, Any
from pydantic import Field, field_validator
from pydantic import BaseModel, ConfigDict

class UOMMasterCreate(BaseModel):
    model_config = ConfigDict(title="UOM - Master Create")
    uom_code: str = Field(min_length=1, max_length=20)
    uom_name: str = Field(min_length=1, max_length=100)
    uom_category: str = Field(min_length=1, max_length=30)
    decimal_places: int = Field(default=0,ge=0,le=10)
    description: Optional[str] = Field(default=None,max_length=250)
    active: bool = True

    @field_validator("uom_name", "uom_code" , "uom_category")
    @classmethod
    def strip_txt (cls,v:str) ->str:
        strip_value = v.strip()
        if not strip_value:
            raise ValueError("Tis Field Is Required")
        return v

    @field_validator("uom_code")
    @classmethod
    def upper_case(cls,v:str) ->str:
        return v.upper()

class UOMMasterUpdate(BaseModel):
    model_config = ConfigDict(title="UOM - Master Update")

    uom_name: Optional[str] = Field(default=None, max_length=100)
    uom_category: Optional[str] = Field(default=None, max_length=30)
    decimal_places: Optional[int] = Field(default=None, ge=0, le=10)
    description: Optional[str] = Field(default=None, max_length=250)
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
    model_config = ConfigDict(
        title="UOM - Response Default Structure"
    )

    success: bool
    message: str
    data: UOMStructure


class UOMResponseList(BaseModel):
    model_config = ConfigDict(
        title="UOM - Response List Default Structure"
    )

    success: bool
    message: str
    data: list[UOMStructure]
