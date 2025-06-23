# app/database.py

# Имитация базы данных пользователей.
# В реальном приложении здесь будет подключение к PostgreSQL, SQLite, и т.д.
# Пароль для user1: "strongpassword1"
# Пароль для user2: "supersecret2"
FAKE_USERS_DB = {
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

def get_user_from_db(username: str) -> dict | None:
    """
    Получение данных пользователя из имитации базы данных.
    """
    return FAKE_USERS_DB.get(username)