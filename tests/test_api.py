from fastapi.testclient import TestClient
from unittest.mock import patch


def test_read_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200

    assert "text/html" in response.headers['content-type']
    assert "<title>Salary Service</title>" in response.text


def test_login_and_get_salary(client: TestClient):
    login_response = client.post(
        "/token", data={"username": "user1", "password": "strongpassword1"}
    )
    assert login_response.status_code == 200
    token_data = login_response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    salary_response = client.get("/users/me/salary", headers=headers)
    assert salary_response.status_code == 200
    salary_data = salary_response.json()
    assert salary_data["salary"] == 60000.0
    assert salary_data["next_raise_date"] == "2024-08-01"


def test_login_wrong_password(client: TestClient):
    response = client.post(
        "/token", data={"username": "user1", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


def test_get_salary_no_token(client: TestClient):
    response = client.get("/users/me/salary")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_get_salary_invalid_token(client: TestClient):
    headers = {"Authorization": "Bearer invalidtoken"}
    response = client.get("/users/me/salary", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"


def test_get_salary_with_token_for_nonexistent_user(client: TestClient):
    """
    Тестирует случай, когда токен валиден, но пользователя уже нет в БД.
    """

    login_response = client.post(
        "/token", data={"username": "user2", "password": "supersecret2"}
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    with patch("app.services.get_user") as mock_get_user:
        mock_get_user.return_value = None

        response = client.get("/users/me/salary", headers=headers)

        assert response.status_code == 401
        assert response.json()["detail"] == "Could not validate credentials"

        mock_get_user.assert_called_with(username="user2")


def test_get_salary_with_malformed_token(client: TestClient):
    """
    Тестирует случай, когда в JWT-токене нет поля 'sub'.
    """
    from app import auth
    from app.core.config import settings
    from datetime import timedelta

    expires_delta = timedelta(minutes=15)
    malformed_token = auth.create_access_token(data={}, expires_delta=expires_delta)
    
    headers = {"Authorization": f"Bearer {malformed_token}"}
    response = client.get("/users/me/salary", headers=headers)

    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"


def test_login_with_nonexistent_user(client: TestClient):
    """
    Проверяет попытку входа несуществующего пользователя.
    """
    response = client.post(
        "/token", data={"username": "ghost", "password": "password"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


def test_get_salary_with_token_without_sub_claim(client: TestClient):

    from app import auth
    from datetime import timedelta

    token_data = {"user_id": 123} 
    expires = timedelta(minutes=15)
    malformed_token = auth.create_access_token(data=token_data, expires_delta=expires)

    headers = {"Authorization": f"Bearer {malformed_token}"}
    response = client.get("/users/me/salary", headers=headers)

    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"

def test_create_access_token_default_expiration():
    """
    Проверяет, что create_access_token без expires_delta создает токен.
    """
    from app import auth
    from jose import jwt
    from app.core.config import settings

    token = auth.create_access_token(data={"sub": "testuser"})
    
    assert isinstance(token, str)

    decoded_payload = jwt.decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    assert decoded_payload["sub"] == "testuser"
    assert "exp" in decoded_payload