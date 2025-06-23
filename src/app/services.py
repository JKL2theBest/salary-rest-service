# src/app/services.py
from typing import Union
from app.models import UserInDB

# Пароль для user1: "strongpassword1"
# Пароль для user2: "supersecret2"
FAKE_USERS_DB: dict[str, dict] = {
    "user1": {
        "username": "user1",
        "hashed_password": "$2b$12$mozSsO55.V.s2e283Rerv.Ro9gFUYERRzDVtWidFLk6iVcNSusFmG",
        "salary": 60000.0,
        "next_raise_date": "2024-08-01",
    },
    "user2": {
        "username": "user2",
        "hashed_password": "$2b$12$sO2wjaxcORjJgDOTo9d95Og595R2h7X6g2XXO5ZhxkZdFKmm/n5nq",
        "salary": 75000.0,
        "next_raise_date": "2024-07-15",
    },
}


def get_user(username: str) -> Union[UserInDB, None]:  # <-- ИЗМЕНЕНО
    """
    Получение данных пользователя из имитации БД.
    """
    if user_data := FAKE_USERS_DB.get(username):
        return UserInDB(**user_data)
    return None
