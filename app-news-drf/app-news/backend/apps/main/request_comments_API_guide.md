- `category_slug`: (будет заполнено автоматически)
- `post_id`: (будет заполнено автоматически)
- `post_slug`: (будет заполнено автоматически)
   - `comment_id`: (будет заполнено автоматически)
   - `parent_comment_id`: (будет заполнено автоматически)

### 2. Настройка авторизации для коллекции
1. Перейдите в настройки коллекции → Authorization
@@ -706,6 +708,590 @@ pm.test("Category info is correct", function () {
});
```

## Тестирование комментариев

### 1. Получение списка всех комментариев
**GET** `{{base_url}}/api/v1/comments/`

**Headers:** (не требуется авторизация)

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Comments list is returned", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('results');
    pm.expect(jsonData.results).to.be.an('array');
});

pm.test("Comment structure is correct", function () {
    var jsonData = pm.response.json();
    if (jsonData.results.length > 0) {
        var comment = jsonData.results[0];
        pm.expect(comment).to.have.property('id');
        pm.expect(comment).to.have.property('content');
        pm.expect(comment).to.have.property('author');
        pm.expect(comment).to.have.property('author_info');
        pm.expect(comment).to.have.property('parent');
        pm.expect(comment).to.have.property('is_active');
        pm.expect(comment).to.have.property('replies_count');
        pm.expect(comment).to.have.property('is_reply');
        pm.expect(comment).to.have.property('created_at');
    }
});
```

### 2. Создание основного комментария
**POST** `{{base_url}}/api/v1/comments/`

**Headers:**
```
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "post": {{post_id}},
    "content": "This is my first comment on this amazing blog post! Thank you for sharing such valuable information."
}
```

**Tests:**
```javascript
pm.test("Status code is 201", function () {
    pm.response.to.have.status(201);
});

pm.test("Comment created successfully", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.content).to.eql("This is my first comment on this amazing blog post! Thank you for sharing such valuable information.");
    pm.expect(jsonData.post).to.eql(pm.environment.get("post_id"));
    pm.expect(jsonData.parent).to.be.null;
    pm.expect(jsonData.is_reply).to.be.false;
    pm.expect(jsonData.is_active).to.be.true;
    
    // Сохраняем ID комментария для дальнейших тестов
    pm.environment.set("comment_id", jsonData.id);
});

pm.test("Author info is included", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.author_info).to.have.property('username');
    pm.expect(jsonData.author_info).to.have.property('full_name');
    pm.expect(jsonData.author_info.username).to.eql("testuser");
});
```

### 3. Создание ответа на комментарий
**POST** `{{base_url}}/api/v1/comments/`

**Headers:**
```
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "post": {{post_id}},
    "parent": {{comment_id}},
    "content": "Thank you for your comment! I'm glad you found the post helpful. Feel free to ask any questions."
}
```

**Tests:**
```javascript
pm.test("Status code is 201", function () {
    pm.response.to.have.status(201);
});

pm.test("Reply comment created successfully", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.content).to.eql("Thank you for your comment! I'm glad you found the post helpful. Feel free to ask any questions.");
    pm.expect(jsonData.post).to.eql(pm.environment.get("post_id"));
    pm.expect(jsonData.parent).to.eql(pm.environment.get("comment_id"));
    pm.expect(jsonData.is_reply).to.be.true;
    pm.expect(jsonData.is_active).to.be.true;
    
    // Сохраняем ID ответа для дальнейших тестов
    pm.environment.set("reply_comment_id", jsonData.id);
});
```

### 4. Получение комментариев к конкретному посту
**GET** `{{base_url}}/api/v1/comments/post/{{post_id}}/`

**Headers:** (не требуется авторизация)

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Post comments data structure is correct", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('post');
    pm.expect(jsonData).to.have.property('comments');
    pm.expect(jsonData).to.have.property('comments_count');
    pm.expect(jsonData.comments).to.be.an('array');
});

pm.test("Post info is included", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.post).to.have.property('id');
    pm.expect(jsonData.post).to.have.property('title');
    pm.expect(jsonData.post).to.have.property('slug');
    pm.expect(jsonData.post.id).to.eql(pm.environment.get("post_id"));
});

pm.test("Comments include replies", function () {
    var jsonData = pm.response.json();
    if (jsonData.comments.length > 0) {
        var mainComment = jsonData.comments.find(comment => comment.parent === null);
        if (mainComment) {
            pm.expect(mainComment).to.have.property('replies');
            pm.expect(mainComment.replies).to.be.an('array');
            pm.expect(mainComment.replies_count).to.be.at.least(0);
        }
    }
});

pm.test("Comments count is correct", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.comments_count).to.be.at.least(1);
});
```

### 5. Получение детального комментария
**GET** `{{base_url}}/api/v1/comments/{{comment_id}}/`

**Headers:** (не требуется авторизация)

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Comment details are correct", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.id).to.eql(pm.environment.get("comment_id"));
    pm.expect(jsonData.content).to.include("This is my first comment");
    pm.expect(jsonData.parent).to.be.null;
    pm.expect(jsonData.is_reply).to.be.false;
});

pm.test("Replies are included for main comment", function () {
    var jsonData = pm.response.json();
    if (jsonData.parent === null) {
        pm.expect(jsonData).to.have.property('replies');
        pm.expect(jsonData.replies).to.be.an('array');
        pm.expect(jsonData.replies_count).to.be.at.least(0);
    }
});
```

### 6. Получение ответов на комментарий
**GET** `{{base_url}}/api/v1/comments/{{comment_id}}/replies/`

**Headers:** (не требуется авторизация)

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Comment replies structure is correct", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('parent_comment');
    pm.expect(jsonData).to.have.property('replies');
    pm.expect(jsonData).to.have.property('replies_count');
    pm.expect(jsonData.replies).to.be.an('array');
});

pm.test("Parent comment info is included", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.parent_comment.id).to.eql(pm.environment.get("comment_id"));
    pm.expect(jsonData.parent_comment).to.have.property('content');
    pm.expect(jsonData.parent_comment).to.have.property('author_info');
});

pm.test("Replies are correct", function () {
    var jsonData = pm.response.json();
    if (jsonData.replies.length > 0) {
        jsonData.replies.forEach(function(reply) {
            pm.expect(reply.parent).to.eql(pm.environment.get("comment_id"));
            pm.expect(reply.is_reply).to.be.true;
            pm.expect(reply).to.have.property('author_info');
        });
    }
});
```

### 7. Обновление комментария
**PATCH** `{{base_url}}/api/v1/comments/{{comment_id}}/`

**Headers:**
```
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "content": "This is my updated first comment on this amazing blog post! Thank you for sharing such valuable information. I've learned a lot from it."
}
```

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Comment updated successfully", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.content).to.eql("This is my updated first comment on this amazing blog post! Thank you for sharing such valuable information. I've learned a lot from it.");
    pm.expect(jsonData.id).to.eql(pm.environment.get("comment_id"));
});
```

### 8. Получение своих комментариев
**GET** `{{base_url}}/api/v1/comments/my-comments/`

**Headers:**
```
Authorization: Bearer {{access_token}}
```

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("My comments are returned", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('results');
    pm.expect(jsonData.results).to.be.an('array');
});

pm.test("All comments belong to current user", function () {
    var jsonData = pm.response.json();
    if (jsonData.results.length > 0) {
        jsonData.results.forEach(function(comment) {
            pm.expect(comment.author_info.username).to.eql("testuser");
        });
    }
});

pm.test("Comments include both main and replies", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.results.length).to.be.at.least(2); // основной комментарий + ответ
    
    var hasMainComment = jsonData.results.some(comment => comment.parent === null);
    var hasReplyComment = jsonData.results.some(comment => comment.parent !== null);
    
    pm.expect(hasMainComment).to.be.true;
    pm.expect(hasReplyComment).to.be.true;
});
```

### 9. Фильтрация комментариев по посту
**GET** `{{base_url}}/api/v1/comments/?post={{post_id}}`

**Headers:** (не требуется авторизация)

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Comments filtered by post", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.results).to.be.an('array');
    if (jsonData.results.length > 0) {
        jsonData.results.forEach(function(comment) {
            // Проверяем через API что комментарий принадлежит нужному посту
            pm.expect(comment).to.have.property('id');
        });
    }
});
```

### 10. Фильтрация комментариев по автору
**GET** `{{base_url}}/api/v1/comments/?author={{user_id}}`

**Headers:** (не требуется авторизация)

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Comments filtered by author", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.results).to.be.an('array');
    if (jsonData.results.length > 0) {
        jsonData.results.forEach(function(comment) {
            pm.expect(comment.author_info.username).to.eql("testuser");
        });
    }
});
```

### 11. Поиск в комментариях
**GET** `{{base_url}}/api/v1/comments/?search=amazing`

**Headers:** (не требуется авторизация)

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Search results are relevant", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.results).to.be.an('array');
    if (jsonData.results.length > 0) {
        var foundRelevant = jsonData.results.some(comment => 
            comment.content.toLowerCase().includes('amazing')
        );
        pm.expect(foundRelevant).to.be.true;
    }
});
```

### 12. Сортировка комментариев
**GET** `{{base_url}}/api/v1/comments/?ordering=created_at`

**Headers:** (не требуется авторизация)

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Comments sorted by creation date ascending", function () {
    var jsonData = pm.response.json();
    if (jsonData.results.length > 1) {
        for (let i = 0; i < jsonData.results.length - 1; i++) {
            var date1 = new Date(jsonData.results[i].created_at);
            var date2 = new Date(jsonData.results[i + 1].created_at);
            pm.expect(date1.getTime()).to.be.at.most(date2.getTime());
        }
    }
});
```

### 13. Фильтрация только основных комментариев (без ответов)
**GET** `{{base_url}}/api/v1/comments/?parent__isnull=true`

**Headers:** (не требуется авторизация)

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Only main comments returned", function () {
    var jsonData = pm.response.json();
    if (jsonData.results.length > 0) {
        jsonData.results.forEach(function(comment) {
            pm.expect(comment.parent).to.be.null;
            pm.expect(comment.is_reply).to.be.false;
        });
    }
});
```

### 14. Мягкое удаление комментария
**DELETE** `{{base_url}}/api/v1/comments/{{comment_id}}/`

**Headers:**
```
Authorization: Bearer {{access_token}}
```

**Tests:**
```javascript
pm.test("Status code is 204", function () {
    pm.response.to.have.status(204);
});

pm.test("Comment is soft deleted", function () {
    // Проверяем что комментарий больше не отображается в активных
    pm.sendRequest({
        url: pm.environment.get("base_url") + "/api/v1/comments/" + pm.environment.get("comment_id") + "/",
        method: 'GET'
    }, function (err, response) {
        pm.expect(response.code).to.eql(404);
    });
});
```

### 15. Создание комментария без авторизации (должно вернуть ошибку)
**POST** `{{base_url}}/api/v1/comments/`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "post": {{post_id}},
    "content": "This should fail without authentication"
}
```

**Tests:**
```javascript
pm.test("Status code is 401", function () {
    pm.response.to.have.status(401);
});

pm.test("Authentication error returned", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('detail');
    pm.expect(jsonData.detail).to.include('credentials');
});
```

### 16. Создание комментария с невалидными данными
**POST** `{{base_url}}/api/v1/comments/`

**Headers:**
```
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "post": 999999,
    "content": ""
}
```

**Tests:**
```javascript
pm.test("Status code is 400", function () {
    pm.response.to.have.status(400);
});

pm.test("Validation errors returned", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.be.an('object');
    // Может содержать ошибки по полям post и content
});
```

### 17. Попытка редактировать чужой комментарий
**PATCH** `{{base_url}}/api/v1/comments/{{other_user_comment_id}}/`

**Headers:**
```
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "content": "Trying to edit someone else's comment"
}
```

**Tests:**
```javascript
pm.test("Status code is 403", function () {
    pm.response.to.have.status(403);
});

pm.test("Permission denied error returned", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('detail');
});
```

### 18. Создание ответа на несуществующий комментарий
**POST** `{{base_url}}/api/v1/comments/`

**Headers:**
```
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "post": {{post_id}},
    "parent": 999999,
    "content": "Reply to non-existent comment"
}
```

**Tests:**
```javascript
pm.test("Status code is 400", function () {
    pm.response.to.have.status(400);
});

pm.test("Validation error for parent comment", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('parent');
});
```

### 19. Создание ответа на комментарий из другого поста
**POST** `{{base_url}}/api/v1/comments/`

**Headers:**
```
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "post": {{another_post_id}},
    "parent": {{comment_id}},
    "content": "Reply to comment from different post"
}
```

**Tests:**
```javascript
pm.test("Status code is 400", function () {
    pm.response.to.have.status(400);
});

pm.test("Validation error for cross-post comment", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('parent');
    pm.expect(jsonData.parent[0]).to.include('same post');
});
```

## Тестирование ошибок

### 1. Создание поста без авторизации
@@ -794,13 +1380,39 @@ Content-Type: application/json
2. **Создание категории** → Сохранение category_id и category_slug
3. **Создание поста** → Сохранение post_id и post_slug
4. **Тестирование CRUD операций с постами**
5. **Тестирование фильтрации и поиска**
6. **Тестирование специальных эндпоинтов** (популярные, последние)
7. **Тестирование ошибок и edge cases**
8. **Удаление тестовых данных**
5. **Создание комментариев** → Сохранение comment_id и reply_comment_id
6. **Тестирование CRUD операций с комментариями**
7. **Тестирование специальных эндпоинтов комментариев**
8. **Тестирование фильтрации и поиска постов и комментариев**
9. **Тестирование специальных эндпоинтов** (популярные, последние)
10. **Тестирование ошибок и edge cases**
11. **Удаление тестовых данных**

## Дополнение к настройкам окружения для комментариев

Добавьте в переменные окружения:
- `user_id`: (ID текущего пользователя, можно получить из профиля)
- `reply_comment_id`: (ID ответа на комментарий)
- `other_user_comment_id`: (ID комментария другого пользователя для тестирования доступа)
- `another_post_id`: (ID другого поста для тестирования валидации)

## Удаление тестовых данных

### Удаление комментариев (мягкое удаление)
**DELETE** `{{base_url}}/api/v1/comments/{{reply_comment_id}}/`

**Headers:**
```
Authorization: Bearer {{access_token}}
```

**Tests:**
```javascript
pm.test("Status code is 204", function () {
    pm.response.to.have.status(204);
});
```

### Удаление поста
**DELETE** `{{base_url}}/api/v1/posts/{{post_slug}}/`

@@ -864,12 +1476,12 @@ python manage.py runserver

## Дополнительные тесты

### Тест пагинации
**GET** `{{base_url}}/api/v1/posts/?page=1&page_size=5`
### Тест пагинации для комментариев
**GET** `{{base_url}}/api/v1/comments/?page=1&page_size=5`

**Tests:**
```javascript
pm.test("Pagination works correctly", function () {
pm.test("Comments pagination works correctly", function () {
var jsonData = pm.response.json();
pm.expect(jsonData).to.have.property('count');
pm.expect(jsonData).to.have.property('next');
@@ -878,19 +1490,44 @@ pm.test("Pagination works correctly", function () {
});
```

### Тест загрузки изображения поста
**PATCH** `{{base_url}}/api/v1/posts/{{post_slug}}/`
### Тест комбинированной фильтрации комментариев
**GET** `{{base_url}}/api/v1/comments/?post={{post_id}}&search=comment&ordering=-created_at`

**Headers:**
```
Authorization: Bearer {{access_token}}
**Tests:**
```javascript
pm.test("Combined comment filtering works", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.results).to.be.an('array');
    if (jsonData.results.length > 0) {
        // Проверяем что результаты содержат искомое слово
        var foundRelevant = jsonData.results.some(comment => 
            comment.content.toLowerCase().includes('comment')
        );
        pm.expect(foundRelevant).to.be.true;
    }
});
```

**Body (form-data):**
- Key: `image`, Type: File, Value: выберите изображение
### Тест структуры вложенных комментариев
**GET** `{{base_url}}/api/v1/comments/post/{{post_id}}/`

### Тест комбинированной фильтрации
**GET** `{{base_url}}/api/v1/posts/?category={{category_id}}&search=blog&ordering=-created_at`
**Tests:**
```javascript
pm.test("Nested comments structure is correct", function () {
    var jsonData = pm.response.json();
    if (jsonData.comments.length > 0) {
        var mainComment = jsonData.comments.find(comment => comment.parent === null);
        if (mainComment && mainComment.replies.length > 0) {
            mainComment.replies.forEach(function(reply) {
                pm.expect(reply.parent).to.eql(mainComment.id);
                pm.expect(reply.is_reply).to.be.true;
                pm.expect(reply).to.have.property('author_info');
                pm.expect(reply).to.have.property('created_at');
            });
        }
    }
});
```

## Автоматизация тестов

@@ -906,10 +1543,25 @@ Authorization: Bearer {{access_token}}
2. Создание категории
3. Создание постов
4. Получение и фильтрация постов
5. Обновление постов
6. Специальные эндпоинты
7. Тестирование ошибок
8. Удаление тестовых данных
9. Выход из системы
5. Создание комментариев и ответов
6. Получение и фильтрация комментариев
7. Обновление постов и комментариев
8. Специальные эндпоинты
9. Тестирование ошибок и валидации
10. Удаление тестовых данных
11. Выход из системы

## Дополнительные URL для комментариев

Не забудьте добавить в ваш `config/urls.py`:

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/posts/', include('apps.main.urls')),
    path('api/v1/auth/', include('apps.accounts.urls')),
    path('api/v1/comments/', include('apps.comments.urls')),  # Добавить эту строку
]
```

Это руководство поможет вам протестировать все функции вашего блог API и убедиться в их корректной работе.
Это руководство поможет вам протестировать все функции вашего блог API включая новое приложение комментариев и убедиться в их корректной работе.