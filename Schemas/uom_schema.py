from datetime import datetime
from typing import Optional
from ninja import Schema
from pydantic import Field, field_validator

class UOMCreateSchema(Schema):
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
            raise ValueError("this field is required")
        return v

    @field_validator("uom_code")
    @classmethod
    def upper_case(cls,v:str) ->str:
        return v.upper()
