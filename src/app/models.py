# src/app/models.py
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None


class UserBase(BaseModel):
    username: str


class UserInDB(UserBase):
    hashed_password: str
    salary: float
    next_raise_date: str


class SalaryInfo(BaseModel):
    salary: float = Field(..., json_schema_extra={"example": 60000.0})
    next_raise_date: str = Field(..., json_schema_extra={"example": "2024-08-01"})

    model_config = ConfigDict(from_attributes=True)
