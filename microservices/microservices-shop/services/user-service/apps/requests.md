# Руководство по тестированию User Service в Postman

## 🚀 Подготовка к тестированию

### Настройка окружения Postman

1. **Создайте новое окружение (Environment)**
   - Name: `User Service Dev`
   - Variables:
     - `base_url`: `http://localhost:8000` (или ваш URL)
     - `access_token`: (оставьте пустым, будет заполняться автоматически)
     - `refresh_token`: (оставьте пустым, будет заполняться автоматически)

### Запуск сервиса

```bash
cd services/user-service
python manage.py runserver 0.0.0.0:8000
```

**⚠️ ВАЖНО: Сначала нужно настроить URL-маршруты!**

В файле `config/urls.py` добавьте:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.authentication.urls')),
    path('api/users/', include('apps.users.urls')),
]
```

## 📋 Коллекция запросов для Postman

### 1. Регистрация пользователя

**POST** `{{base_url}}/api/users/register/`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "email": "test@example.com",
    "username": "testuser",
    "first_name": "Иван",
    "last_name": "Иванов",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!"
}
```

**Ожидаемый ответ (201):**
```json
{
    "id": 1,
    "email": "test@example.com",
    "username": "testuser",
    "first_name": "Иван",
    "last_name": "Иванов",
    "is_active": true,
    "date_joined": "2025-09-09T12:00:00Z"
}
```

**Tests (вкладка Tests в Postman):**
```javascript
pm.test("User registration successful", function () {
    pm.response.to.have.status(201);
    pm.response.to.be.json;

    const responseJson = pm.response.json();
    pm.expect(responseJson).to.have.property('id');
    pm.expect(responseJson).to.have.property('email');
    pm.expect(responseJson.email).to.equal('test@example.com');
});
```

### 2. Авторизация пользователя

**POST** `{{base_url}}/api/auth/login/`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "email": "test@example.com",
    "password": "SecurePass123!"
}
```

**Ожидаемый ответ (200):**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": 1,
        "email": "test@example.com",
        "username": "testuser",
        "first_name": "Иван",
        "last_name": "Иванов"
    }
}
```

**Tests:**
```javascript
pm.test("Login successful", function () {
    pm.response.to.have.status(200);
    pm.response.to.be.json;

    const responseJson = pm.response.json();
    pm.expect(responseJson).to.have.property('access');
    pm.expect(responseJson).to.have.property('refresh');
    pm.expect(responseJson).to.have.property('user');

    // Сохраняем токены в переменные окружения
    pm.environment.set("access_token", responseJson.access);
    pm.environment.set("refresh_token", responseJson.refresh);
});
```

### 3. Получение профиля пользователя

**GET** `{{base_url}}/api/users/profile/`

**Headers:**
```
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

**Ожидаемый ответ (200):**
```json
{
    "phone": "",
    "address": "",
    "date_of_birth": null
}
```

**Tests:**
```javascript
pm.test("Profile retrieved successfully", function () {
    pm.response.to.have.status(200);
    pm.response.to.be.json;

    const responseJson = pm.response.json();
    pm.expect(responseJson).to.have.property('phone');
    pm.expect(responseJson).to.have.property('address');
    pm.expect(responseJson).to.have.property('date_of_birth');
});
```

### 4. Обновление профиля пользователя

**PUT** `{{base_url}}/api/users/profile/update/`

**Headers:**
```
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "phone": "+7-900-123-45-67",
    "address": "г. Москва, ул. Пушкина, д. 10",
    "date_of_birth": "1990-01-15"
}
```

**Ожидаемый ответ (200):**
```json
{
    "phone": "+7-900-123-45-67",
    "address": "г. Москва, ул. Пушкина, д. 10",
    "date_of_birth": "1990-01-15"
}
```

**Tests:**
```javascript
pm.test("Profile updated successfully", function () {
    pm.response.to.have.status(200);
    pm.response.to.be.json;

    const responseJson = pm.response.json();
    pm.expect(responseJson.phone).to.equal("+7-900-123-45-67");
    pm.expect(responseJson.address).to.equal("г. Москва, ул. Пушкина, д. 10");
    pm.expect(responseJson.date_of_birth).to.equal("1990-01-15");
});
```

### 5. Обновление токена доступа

**POST** `{{base_url}}/api/auth/refresh/`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "refresh": "{{refresh_token}}"
}
```

**Ожидаемый ответ (200):**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Tests:**
```javascript
pm.test("Token refreshed successfully", function () {
    pm.response.to.have.status(200);
    pm.response.to.be.json;

    const responseJson = pm.response.json();
    pm.expect(responseJson).to.have.property('access');

    // Обновляем токен в переменных окружения
    pm.environment.set("access_token", responseJson.access);
});
```

## 🧪 Тест-кейсы для проверки ошибок

### 6. Регистрация с некорректными данными

**POST** `{{base_url}}/api/users/register/`

**Body (JSON) - пароли не совпадают:**
```json
{
    "email": "test2@example.com",
    "username": "testuser2",
    "first_name": "Петр",
    "last_name": "Петров",
    "password": "SecurePass123!",
    "password_confirm": "DifferentPass123!"
}
```

**Ожидаемый ответ (400):**
```json
{
    "non_field_errors": ["Passwords do not match"]
}
```

### 7. Авторизация с неверными данными

**POST** `{{base_url}}/api/auth/login/`

**Body (JSON):**
```json
{
    "email": "wrong@example.com",
    "password": "wrongpassword"
}
```

**Ожидаемый ответ (401):**
```json
{
    "error": "Invalid credentials"
}
```

### 8. Доступ без токена авторизации

**GET** `{{base_url}}/api/users/profile/`

**Headers:** (без Authorization)
```
Content-Type: application/json
```

**Ожидаемый ответ (401):**
```json
{
    "detail": "Authentication credentials were not provided."
}
```

## 🚀 Быстрый запуск тестов

### Создание Collection Runner

1. Создайте коллекцию со всеми запросами выше
2. Установите порядок выполнения:
   - Регистрация пользователя
   - Авторизация пользователя
   - Получение профиля
   - Обновление профиля
   - Обновление токена

3. Запустите Collection Runner для автоматического тестирования

## 📊 Pre-request Scripts

Для автоматической настройки данных добавьте в Pre-request Script:

```javascript
// Генерация случайных данных для тестирования
const randomEmail = `test${Math.floor(Math.random() * 10000)}@example.com`;
const randomUsername = `user${Math.floor(Math.random() * 10000)}`;

pm.environment.set("random_email", randomEmail);
pm.environment.set("random_username", randomUsername);
```

## ⚠️ Устранение проблем

### Проблема: "CSRF verification failed"
**Решение:** Убедитесь, что в настройках Django отключена CSRF-защита для API:
```python
# В settings.py
CSRF_TRUSTED_ORIGINS = ['http://localhost:3000']
```

### Проблема: CORS ошибки
**Решение:** Проверьте настройки CORS в `settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    # добавьте другие домены
]
```

### Проблема: Токен истек
**Решение:** Используйте запрос обновления токена перед основными запросами

## 📝 Дополнительные тесты

Создайте дополнительные тест-кейсы для:

- Регистрации пользователя с уже существующим email
- Проверки валидации полей (короткий пароль, неверный формат email)
- Тестирования с истекшими токенами
- Проверки обновления только части профиля
- Тестирования с различными часовыми поясами для дат

Это руководство поможет вам полностью протестировать функциональность вашего User Service!



<!--from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from apps.users.models import User

@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request) -> Response:
    # Ensure the request is JSON
    if not request.content_type.startswith('application/json'):
        return Response(
            {"error": "Request must be JSON"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Get and normalize inputs
    email = request.data.get("email", "").strip().lower()  # Trim and lowercase
    password = request.data.get("password", "").strip()    # Trim password

    print(f"Received email: '{email}' (length: {len(email)})")  # Debug
    print(f"Received password: '{password}' (length: {len(password)})")  # Debug

    if not email or not password:
        return Response(
            {"error": "Email and password are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(username=email, password=password)
    print(f"Authenticated user: {user} (is_active: {user.is_active if user else 'N/A'})")  # Debug

    if user and user.is_active:
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "username": user.username,
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
        )

    return Response(
        {"error": "Invalid credentials"},
        status=status.HTTP_401_UNAUTHORIZED
    )-->
