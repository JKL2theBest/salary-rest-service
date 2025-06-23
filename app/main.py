# app/main.py
from fastapi import FastAPI
from . import routes

def create_app() -> FastAPI:
    """
    Фабрика для создания экземпляра FastAPI приложения.
    """
    app = FastAPI(
        title="Salary Viewing Service",
        description="A service to view your salary and next raise date securely.",
        version="1.0.0"
    )

    # Подключаем роутер с эндпоинтами
    app.include_router(routes.router)

    @app.get("/", tags=["Root"])
    async def read_root():
        """Корневой эндпоинт для проверки работоспособности сервиса."""
        return {"message": "Welcome to the Salary Service API"}

    return app

app = create_app()