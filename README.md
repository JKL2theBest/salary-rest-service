# Сервис просмотра зарплаты

Этот проект представляет собой REST-сервис для просмотра текущей зарплаты и даты следующего повышения. Каждый сотрудник может видеть только свои данные. Доступ к защищенным данным осуществляется с помощью JWT токенов.

## Технологический стек

*   **FastAPI**: для создания REST API.
*   **Poetry**: для управления зависимостями.
*   **Pytest**: для тестирования.
*   **Docker**: для контейнеризации приложения.
*   **GitLab CI/CD**: для автоматизации тестирования и сборки.

## Инструкция по запуску (локально)

1.  **Клонируйте репозиторий:**
    ```bash
    git clone <your-repo-url>
    cd salary-rest-service
    ```

2.  **Установите Poetry** (если он еще не установлен):
    ```bash
    pip install poetry
    ```

3.  **Установите зависимости проекта:**
    ```bash
    poetry install
    ```

4.  **Запустите сервис:**
    ```bash
    poetry run uvicorn app.main:app --reload
    ```
    Сервис будет доступен по адресу `http://127.0.0.1:8000`. Интерактивная документация (Swagger UI) будет доступна по адресу `http://127.0.0.1:8000/docs`.

## Инструкция по запуску (Docker)

1.  **Соберите Docker-образ:**
    ```bash
    docker build -t salary-rest-service .
    ```

2.  **Запустите контейнер:**
    ```bash
    docker run -d --name salary-app -p 8000:8000 salary-rest-service
    ```
    Сервис будет доступен по адресу `http://127.0.0.1:8000`.

## Взаимодействие с API

В системе есть два тестовых пользователя:
*   `user1` с паролем `strongpassword1`
*   `user2` с паролем `supersecret2`

### 1. Получение токена доступа

Отправьте POST-запрос на `/token` с вашими учетными данными.

```bash
curl -X POST "http://127.0.0.1:8000/token" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=user1&password=strongpassword1"
```

**Ответ:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 2. Получение данных о зарплате

Отправьте GET-запрос на `/users/me/salary`, используя полученный токен в заголовке `Authorization`.

> **Примечание**: Замените `YOUR_TOKEN` на токен, полученный на предыдущем шаге.

```bash
curl -X GET "http://127.0.0.1:8000/users/me/salary" \
-H "Authorization: Bearer YOUR_TOKEN"
```

**Ответ для `user1`:**
```json
{
  "salary": 60000,
  "next_raise_date": "2024-08-01"
}
```

### 3. Пример ошибки (неверный токен)

```bash
curl -X GET "http://127.0.0.1:8000/users/me/salary" \
-H "Authorization: Bearer invalidtoken"
```

**Ответ:**
```json
{
  "detail": "Could not validate credentials"
}
```

## Запуск тестов

Для запуска тестов выполните команду:
```bash
poetry run pytest
```