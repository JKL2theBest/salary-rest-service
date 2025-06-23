# app/models.py
from datetime import date
from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    """Модель ответа с токеном доступа."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Модель данных, закодированных в JWT токене."""
    username: Optional[str] = None

class User(BaseModel):
    """Базовая модель пользователя."""
    username: str

class UserInDB(User):
    """Модель пользователя, как он хранится в БД (с хэшем пароля)."""
    hashed_password: str
    salary: float
    next_raise_date: date

class SalaryInfo(BaseModel):
    """Модель для ответа с информацией о зарплате."""
    salary: float
    next_raise_date: date