# src/app/main.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from pathlib import Path  # <-- 1. Импортируем Path
from app import api

# 2. Определяем путь к директории, где находится этот файл (main.py)
BASE_DIR = Path(__file__).resolve().parent

# 3. Настраиваем шаблонизатор и статику, используя абсолютные пути
templates = Jinja2Templates(directory=BASE_DIR / "templates")

app = FastAPI(
    title="Salary Viewing Service",
    description="A service to view your salary and next raise date securely.",
    version="0.1.0",
)

# Монтируем статику, используя абсолютный путь
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

app.include_router(api.router)


@app.get("/", response_class=HTMLResponse, tags=["Root"])
def read_root(request: Request):
    """
    Корневой эндпоинт, который отображает приветственную HTML-страницу.
    """
    return templates.TemplateResponse(request, "index.html")