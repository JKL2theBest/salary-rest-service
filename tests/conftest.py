# tests/conftest.py
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")
def client() -> TestClient:
    """
    Фикстура для создания тестового клиента FastAPI.
    """
    return TestClient(app)
