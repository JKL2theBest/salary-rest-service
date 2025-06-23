# tests/test_main.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Salary Service API"}

def test_login_and_get_salary():
    # 1. Попытка входа с верными данными
    login_response = client.post(
        "/token",
        data={"username": "user1", "password": "strongpassword1"}
    )
    assert login_response.status_code == 200
    token_data = login_response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
    
    token = token_data["access_token"]
    
    # 2. Запрос данных о зарплате с полученным токеном
    headers = {"Authorization": f"Bearer {token}"}
    salary_response = client.get("/users/me/salary", headers=headers)
    
    assert salary_response.status_code == 200
    salary_data = salary_response.json()
    assert salary_data["salary"] == 60000.0
    assert salary_data["next_raise_date"] == "2024-08-01"

def test_login_wrong_password():
    response = client.post(
        "/token",
        data={"username": "user1", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

def test_get_salary_no_token():
    response = client.get("/users/me/salary")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_get_salary_invalid_token():
    headers = {"Authorization": "Bearer invalidtoken"}
    response = client.get("/users/me/salary", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"