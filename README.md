# Salary service

Проект представляет собой REST-сервис для просмотра текущей зарплаты и даты следующего повышения. Каждый сотрудник может видеть только свои данные. Доступ к защищенным данным осуществляется с помощью JWT токенов.

## Технологический стек

*   **FastAPI**: для создания REST API.
*   **Poetry**: для управления зависимостями.
*   **Pytest**: для тестирования.
*   **Docker**: для контейнеризации.

## Установка и запуск

Можно запустить двумя способами: локально с помощью Poetry или в контейнере Docker.

### Шаг 1

#### 1.1. Клонируйте репозиторий
```bash
git clone https://gitlab.com/JKL2theBest/salary-rest-service
cd salary-rest-service
```

#### 1.2. Настройте переменные окружения

1.  Найдите в проекте файл `.env.example`. Он выглядит так:
    ```ini
    # .env.example
    SECRET_KEY=""
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ALGORITHM="HS256"
    ```
2.  Скопируйте этот файл и назовите копию `.env`:
    ```bash
    cp .env.example .env
    ```
3.  Сгенерируйте секретный ключ:
    ```bash
    python -c 'import secrets; print(secrets.token_hex(32))'
    ```
4.  Вставьте его в файл `.env`:
    ```ini
    # .env
    SECRET_KEY="e9a3f8c1b5d7e6f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0"
    ...
    ```

### Шаг 2 (Вариант А): Poetry

1.  **Установите зависимости проекта:**
    ```bash
    poetry install
    ```
2.  **Запустите веб-сервис:**
    ```bash
    poetry run uvicorn app.main:app --reload --app-dir src --port 8001
    ```
    *   Стандартный порт 8000 часто занят другими программами, поэтому 8001 — более надежный выбор.

*   **Готово!** Сервис доступен по адресу:
*   `http://127.0.0.1:8001`
*   **(Swagger UI)**: `http://127.0.0.1:8001/docs`

### Шаг 2 (Вариант Б): Docker

1.  **Соберите Docker-образ:**
    ```bash
    docker build -t salary-rest-service .
    ```
2.  **Запустите контейнер:**
    ```bash
    docker run -d -p 8001:8000 --name salary-app salary-rest-service
    ```

*   **Готово!** Сервис доступен по адресу `http://127.0.0.1:8001`.

Чтобы остановить контейнер, выполните: `docker stop salary-app`.

## Тестирование

Тесты написаны с `pytest`.

#### Запуск всех тестов
```bash
poetry run pytest
```

#### Запуск тестов с отчетом о покрытии
```bash
poetry run pytest --cov=app --cov-report=term-missing
```

#### Флаг `-v` (verbose) выведет названия каждого выполняемого теста
```bash
poetry run pytest -v
```

## Взаимодействие с API

Вы можете взаимодействовать с API через интерактивную документацию (`http://127.0.0.1:8001/docs`) или с помощью утилиты `curl` в терминале.

**Тестовые пользователи:**
*   **Логин:** `user1` / **Пароль:** `strongpassword1`
*   **Логин:** `user2` / **Пароль:** `supersecret2`

> **Примечание**: В командах ниже используется порт `8001`. Если вы запускали сервис на другом порту, измените его.

### 1. Получение токена доступа
```bash
curl -X POST "http://127.0.0.1:8001/token" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=user1&password=strongpassword1"
```
**Ответ:**
```json
{
  "access_token": "eyJhbGciOiJI...",
  "token_type": "bearer"
}
```

### 2. Получение данных о зарплате
Скопируйте `access_token` из ответа выше и подставьте его в следующую команду вместо `YOUR_TOKEN`.

```bash
curl -X GET "http://127.0.0.1:8001/users/me/salary" \
-H "Authorization: Bearer YOUR_TOKEN"
```
**Ответ:**
```json
{
  "salary": 60000.0,
  "next_raise_date": "2024-08-01"
}
```