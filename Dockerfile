FROM python:3.11-slim AS builder

ENV POETRY_VERSION=1.8.2 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY poetry.lock pyproject.toml ./

# Only production-dependencies
RUN poetry install --no-dev --no-interaction --no-ansi

# --- Runtime ---
FROM python:3.11-slim

RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /home/appuser

COPY --from=builder /app/ /usr/local/

COPY --chown=appuser:appuser ./src/app ./app

USER appuser

EXPOSE 8000

# Run command
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]