# Руководство по тестированию API в Postman

## Настройка окружения

### 1. Создание коллекции
1. Откройте Postman
2. Создайте новую коллекцию: `Django Auth API`
3. В настройках коллекции добавьте переменные:
   - `base_url`: `http://127.0.0.1:8000`
   - `access_token`: (будет заполнено автоматически)
   - `refresh_token`: (будет заполнено автоматически)

### 2. Настройка авторизации для коллекции
1. Перейдите в настройки коллекции → Authorization
2. Выберите Type: `Bearer Token`
3. В поле Token введите: `{{access_token}}`

## Тестирование эндпоинтов

### 1. Регистрация пользователя
**POST** `{{base_url}}/api/v1/auth/register/`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPassword123!",
    "password_confirm": "TestPassword123!",
    "first_name": "Test",
    "last_name": "User"
}
```

**Tests (вкладка Tests):**
```javascript
pm.test("Status code is 201", function () {
    pm.response.to.have.status(201);
});

pm.test("Response contains tokens", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('access');
    pm.expect(jsonData).to.have.property('refresh');
    pm.expect(jsonData).to.have.property('user');
    
    // Сохраняем токены в переменные окружения
    pm.environment.set("access_token", jsonData.access);
    pm.environment.set("refresh_token", jsonData.refresh);
});

pm.test("User data is correct", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.user.email).to.eql("test@example.com");
    pm.expect(jsonData.user.username).to.eql("testuser");
});
```

### 2. Вход пользователя
**POST** `{{base_url}}/api/v1/auth/login/`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "email": "test@example.com",
    "password": "TestPassword123!"
}
```

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Login successful", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.message).to.eql("User login successfully");
    
    // Обновляем токены
    pm.environment.set("access_token", jsonData.access);
    pm.environment.set("refresh_token", jsonData.refresh);
});
```

### 3. Получение профиля пользователя
**GET** `{{base_url}}/api/v1/auth/profile/`

**Headers:**
```
Authorization: Bearer {{access_token}}
```

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Profile data is returned", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('id');
    pm.expect(jsonData).to.have.property('email');
    pm.expect(jsonData).to.have.property('posts_count');
    pm.expect(jsonData).to.have.property('comments_count');
});
```

### 4. Обновление профиля
**PATCH** `{{base_url}}/api/v1/auth/profile/`

**Headers:**
```
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "first_name": "Updated",
    "last_name": "Name",
    "bio": "This is my updated bio"
}
```

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Profile updated successfully", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.first_name).to.eql("Updated");
    pm.expect(jsonData.last_name).to.eql("Name");
    pm.expect(jsonData.bio).to.eql("This is my updated bio");
});
```

### 5. Смена пароля
**PUT** `{{base_url}}/api/v1/auth/change-password/`

**Headers:**
```
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "old_password": "TestPassword123!",
    "new_password": "NewTestPassword123!",
    "new_password_confirm": "NewTestPassword123!"
}
```

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Password changed successfully", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.message).to.eql("Password changed successfully");
});
```

### 6. Обновление токена
**POST** `{{base_url}}/api/v1/auth/token/refresh/`

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

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("New access token received", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('access');
    pm.environment.set("access_token", jsonData.access);
});
```

### 7. Выход из системы
**POST** `{{base_url}}/api/v1/auth/logout/`

**Headers:**
```
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "refresh_token": "{{refresh_token}}"
}
```

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Logout successful", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.message).to.eql("Logout successful");
    
    // Очищаем токены
    pm.environment.unset("access_token");
    pm.environment.unset("refresh_token");
});
```

## Тестирование ошибок

### 1. Регистрация с невалидными данными
**POST** `{{base_url}}/api/v1/auth/register/`

**Body (JSON) - Несовпадающие пароли:**
```json
{
    "username": "testuser2",
    "email": "test2@example.com",
    "password": "TestPassword123!",
    "password_confirm": "DifferentPassword123!",
    "first_name": "Test",
    "last_name": "User"
}
```

**Expected:** Status 400, ошибка валидации паролей

### 2. Вход с неверными данными
**POST** `{{base_url}}/api/v1/auth/login/`

**Body (JSON):**
```json
{
    "email": "test@example.com",
    "password": "WrongPassword"
}
```

**Expected:** Status 400, ошибка аутентификации

### 3. Доступ к защищенному эндпоинту без токена
**GET** `{{base_url}}/api/v1/auth/profile/`

**Headers:** (без Authorization)

**Expected:** Status 401, ошибка аутентификации

### 4. Использование недействительного токена
**GET** `{{base_url}}/api/v1/auth/profile/`

**Headers:**
```
Authorization: Bearer invalid_token
```

**Expected:** Status 401, недействительный токен

## Последовательность тестирования

1. **Регистрация** → Получение токенов
2. **Вход** → Обновление токенов  
3. **Получение профиля** → Проверка данных
4. **Обновление профиля** → Проверка изменений
5. **Смена пароля** → Проверка успешности
6. **Обновление токена** → Получение нового access_token
7. **Выход** → Очистка токенов

## Создание тестового набора

### Pre-request Script для коллекции:
```javascript
// Проверяем, запущен ли Django сервер
pm.sendRequest({
    url: pm.environment.get("base_url"),
    method: 'GET'
}, function (err, response) {
    if (err) {
        console.log("Django server is not running on " + pm.environment.get("base_url"));
    }
});
```

### Collection Tests:
```javascript
pm.test("Django server is accessible", function () {
    pm.response.to.not.be.error;
});
```

## Запуск Django сервера

Перед тестированием убедитесь, что Django сервер запущен:

```bash
# В терминале
python manage.py runserver
```

## Дополнительные тесты

### Тест загрузки аватара
**PATCH** `{{base_url}}/api/v1/auth/profile/`

**Headers:**
```
Authorization: Bearer {{access_token}}
```

**Body (form-data):**
- Key: `avatar`, Type: File, Value: выберите изображение
- Key: `bio`, Type: Text, Value: "Updated bio with avatar"

### Тест с большими данными
Проверьте ограничения полей (например, bio до 500 символов)

## Автоматизация тестов

Для автоматического запуска всех тестов используйте Collection Runner:
1. Нажмите на коллекцию → Run collection
2. Выберите все запросы
3. Установите задержку между запросами (500ms)
4. Запустите тесты

Это руководство поможет вам протестировать все функции вашего API и убедиться в их корректной работе.