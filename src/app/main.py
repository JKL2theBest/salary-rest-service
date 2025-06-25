from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from pathlib import Path
from app import api

BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(directory=BASE_DIR / "templates")

app = FastAPI(
    title="Salary Viewing Service",
    description="A service to view your salary and next raise date securely.",
    version="0.1.0",
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

app.include_router(api.router)


@app.get("/", response_class=HTMLResponse, tags=["Root"])
def read_root(request: Request):
    """
    Корневой эндпоинт, который отображает приветственную HTML-страницу.
    """
    return templates.TemplateResponse(request, "index.html")
