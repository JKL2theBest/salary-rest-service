# Сервис просмотра зарплаты

Этот проект представляет собой REST-сервис для просмотра текущей зарплаты и даты следующего повышения. Каждый сотрудник может видеть только свои данные. Доступ к защищенным данным осуществляется с помощью JWT токенов.

## Технологический стек

*   **FastAPI**: для создания REST API.
*   **Poetry**: для управления зависимостями.
*   **Pytest**: для тестирования.
*   **Docker**: для контейнеризации приложения.
*   **GitLab CI/CD**: для автоматизации тестирования и сборки.

## Структура проекта

```
.
├── src/
│   └── app/
│       ├── __init__.py
│       ├── api.py
│       ├── auth.py
│       ├── core/
│       │   └── config.py
│       ├── main.py
│       ├── models.py
│       └── services.py
├── tests/
├── .env
├── .gitignore
├── .gitlab-ci.yml
├── Dockerfile
├── pyproject.toml
└── README.md
```

## Установка и запуск

### 1. Предварительные требования
- Python 3.9+
- Poetry
- Docker (опционально, для запуска в контейнере)

### 2. Конфигурация
Перед первым запуском создайте файл `.env` в корне проекта, скопировав в него содержимое из `.env.example` (если он есть) или создав с нуля:
```ini
# .env
SECRET_KEY="<your_super_secret_key_here>"
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM="HS256"
```
> **Важно**: В реальном проекте `.env` файл не должен попадать в Git. Убедитесь, что он добавлен в `.gitignore`.

### 3. Запуск локально
1.  **Клонируйте репозиторий:**
    ```bash
    git clone <your-repo-url>
    cd salary-rest-service
    ```
2.  **Установите зависимости:**
    ```bash
    poetry install
    ```
3.  **Запустите сервис:**
    ```bash
    poetry run uvicorn app.main:app --reload --app-dir src
    poetry run uvicorn app.main:app --reload --app-dir src --port 8001
    ```
    Сервис будет доступен по адресу `http://127.0.0.1:8000`. Интерактивная документация (Swagger UI) — `http://127.0.0.1:8000/docs`.

### 4. Запуск в Docker
1.  **Соберите Docker-образ:**
    ```bash
    docker build -t salary-service .
    ```
2.  **Запустите контейнер:**
    ```bash
    docker run -d --name salary-app -p 8000:8000 salary-service
    docker run -d -p 8001:8000 --name salary-app salary-rest-service
    ```

## Тестирование
Для запуска тестов и просмотра отчета о покрытии выполните:
```bash
poetry run pytest --cov=app --cov-report=term-missing
```

## Взаимодействие с API

В системе есть два тестовых пользователя:
*   `user1` с паролем `strongpassword1`
*   `user2` с паролем `supersecret2`

### 1. Получение токена доступа
```bash
curl -X POST "http://127.0.0.1:8000/token" -H "Content-Type: application/x-www-form-urlencoded" -d "username=user1&password=strongpassword1"
```

### 2. Получение данных о зарплате
Замените `YOUR_TOKEN` на токен, полученный на предыдущем шаге.
```bash
curl -X GET "http://127.0.0.1:8000/users/me/salary" -H "Authorization: Bearer YOUR_TOKEN"
```