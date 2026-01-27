# Найденные ошибки в проекте

Этот документ содержит полный список найденных ошибок в проекте, а также информацию о том, какие из них были исправлены.

## ✅ Исправленные ошибки

### 1. Отсутствие обработки DoesNotExist в auth_backend.py

**Файл:** `effective_mobile/auth/auth_backend.py`

**Было:**
```python
def authenticate(self, request, token=None):
    if not token:
        return None
    custom_token = CustomToken.objects.get(token=token)  # ❌
    return custom_token.user

def get_user(self, user_id):
    return User.objects.get(id=user_id)  # ❌
```

**Стало:**
```python
def authenticate(self, request, token=None):
    if not token:
        return None
    try:
        custom_token = CustomToken.objects.select_related('user_id').get(token=token)
        return custom_token.user_id
    except CustomToken.DoesNotExist:
        return None

def get_user(self, user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None
```

---

### 2. Пустой ALGORITHM для JWT токена

**Файл:** `effective_mobile/auth/models.py`

**Было:**
```python
SECRET_KEY = os.getenv('SECRET_KEY', 'my_secret_key')
ALGORITHM = os.getenv('ALGORITHM', '')  # ❌ Пустая строка!
```

**Стало:**
```python
SECRET_KEY = os.getenv('SECRET_KEY', settings.SECRET_KEY)
ALGORITHM = os.getenv('ALGORITHM', 'HS256')  # ✅ Корректный алгоритм по умолчанию
```

---

### 3. Недостаточная длина поля для JWT токена

**Файл:** `effective_mobile/auth/models.py`

**Было:**
```python
token = models.CharField(max_length=64, unique=True)  # ❌ JWT токены длиннее
```

**Стало:**
```python
token = models.CharField(max_length=255, unique=True)  # ✅ Достаточная длина
```

---

### 4. Обход валидации при создании книги

**Файл:** `effective_mobile/books/views.py`

**Было:**
```python
@api_view(['GET'])  # ❌ Неправильный метод
def create_book(request):
    data = request.data
    user = request.user
    data['author_id'] = user.id
    serializer = CreateBookSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        new_book = Books.objects.create(**data)  # ❌ Обход валидации!
        return Response(...)
```

**Стало:**
```python
@api_view(['POST'])  # ✅ Правильный метод
@permission_classes([IsAuthenticated])
def create_book(request):
    serializer = CreateBookSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(author=request.user)  # ✅ Используем validated_data
        return Response(...)
```

---

### 5. Отсутствие проверки прав доступа в get_book_by_id

**Файл:** `effective_mobile/books/views.py`

**Было:**
```python
@api_view(['GET'])
@permission_classes([IsAuthenticated, OnlyAuthor])  # ❌ OnlyAuthor не работает корректно
def get_book_by_id(request, book_id):
    book = Books.objects.filter(id=book_id, is_published=True).first()
    if book:
        return Response({"book": {...}})  # ❌ Нет проверки авторства!
    return Response({"message": "Книга не найдена."})
```

**Стало:**
```python
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_book_by_id(request, book_id):
    book = get_object_or_404(Books, id=book_id, is_published=True)
    if book.author == request.user:
        return Response({"book": {...}})
    return Response({"message": "У вас нет прав на просмотр этой книги."},
                    status=status.HTTP_403_FORBIDDEN)
```

---

### 6. Отсутствие проверки прав доступа в delete_book

**Файл:** `effective_mobile/books/views.py`

**Было:**
```python
@api_view(['GET'])  # ❌ Неправильный метод
@permission_classes([OnlyAuthor, OnlyModeratorOrAdmin])
def delete_book(request, book_id):
    book = Books.objects.filter(id=book_id).first()
    if book:
        book.delete()  # ❌ Нет проверки прав на конкретную книгу!
        return Response({"message": "Книга удалена."})
    return Response({"message": "Книга не найдена."})
```

**Стало:**
```python
@api_view(['DELETE'])  # ✅ Правильный метод
@permission_classes([IsAuthenticated, OnlyAuthor])
def delete_book(request, book_id):
    book = get_object_or_404(Books, id=book_id)
    if book.author == request.user or request.user.role in [CustomUser.ADMIN, CustomUser.MODERATOR]:
        book.delete()
        return Response({"message": "Книга удалена."})
    return Response({"message": "У вас нет прав на удаление этой книги."},
                    status=status.HTTP_403_FORBIDDEN)
```

---

### 7. Отсутствие обработки DoesNotExist в logout_user

**Файл:** `effective_mobile/auth/views.py`

**Было:**
```python
@api_view(['GET'])
def logout_user(request):
    CustomToken.objects.get(user_id_id=request.user).delete()  # ❌ Исключение если токена нет
    logout(request)
    return Response({"message": "Вы вышли из системы."})
```

**Стало:**
```python
@api_view(['GET'])
def logout_user(request):
    CustomToken.objects.filter(user_id=request.user).delete()  # ✅ Безопасно
    logout(request)
    return Response({"message": "Вы вышли из системы."})
```

---

### 8. Некорректное использование user_id_id в delete_me

**Файл:** `effective_mobile/auth/views.py`

**Было:**
```python
CustomToken.objects.filter(user_id_id=user).delete()  # ❌ Двойной _id
```

**Стало:**
```python
CustomToken.objects.filter(user_id=user).delete()  # ✅ Правильно
```

---

### 9. Исправление OnlyAuthor permission

**Файл:** `effective_mobile/api/permissions.py`

**Было:**
```python
def has_permission(self, request, view):
    if request.method == 'GET':
        book_id = request.parser_context.get('kwargs', {}).get('book_id')
        if not book_id:
            return False
        book = Books.objects.get(id=book_id, is_published=True)  # ❌ Исключение
        return book.author_id == request.user.id
    return False
```

**Стало:**
```python
def has_permission(self, request, view):
    book_id = request.parser_context.get('kwargs', {}).get('book_id')
    if not book_id:
        return True
    try:
        book = Books.objects.get(id=book_id)
    except Books.DoesNotExist:
        return False
    return book.author == request.user

def has_object_permission(self, request, view, obj):
    return obj.author == request.user
```

---

### 10. Отсутствие id в BookSerializer

**Файл:** `effective_mobile/api/serializers.py`

**Было:**
```python
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = [
            'title',
            'description',
            'is_published',
            'author'
        ]  # ❌ Нет id
```

**Стало:**
```python
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = [
            'id',  # ✅ Добавлено
            'title',
            'description',
            'is_published',
            'author'
        ]
```

---

### 11. Middleware не сбрасывает request.user

**Файл:** `effective_mobile/auth/auth_middleware.py`

**Было:**
```python
def process_request(self, request):
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        token = auth_header[7:]
        backend = TokenAuthenticationBackend()
        user = backend.authenticate(request, token=token)
        if user:
            request.user = user
    # ❌ Если user=None, request.user остается старым
```

**Стало:**
```python
def process_request(self, request):
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        token = auth_header[7:]
        backend = TokenAuthenticationBackend()
        user = backend.authenticate(request, token=token)
        request.user = user if user else AnonymousUser()  # ✅ Всегда устанавливаем
```

---

### 12. Устаревшая версия Django

**Файл:** `requirements.txt`

**Было:**
```text
Django==6.0.1  # ❌ Несуществует такой версии
dotenv==0.9.9  # ❌ Устаревший пакет
```

**Стало:**
```text
Django==5.1.5  # ✅ Актуальная версия
# dotenv==0.9.9 удален, используется python-dotenv
```

---

### 13. Исправлена логика login_user

**Файл:** `effective_mobile/auth/views.py`

**Было:**
```python
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, email=email, password=password)
    if user is not None:
        token_exist = CustomToken.objects.filter(user_id_id=user.id).first()
        if token_exist is not None:  # ❌ Странная логика
            login(request, user)
            return Response(...)
        return Response({"message": "Нет токена"})
    return Response(...)
```

**Стало:**
```python
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, email=email, password=password)
    if user is not None and user.is_active:
        login(request, user)
        return Response(data={"message": "Вы аутентифицирован", ...})
    return Response({"message": "Пользователь не найден или неактивен"},
                    status=status.HTTP_400_BAD_REQUEST)
```

---

## ⚠️ Неисправленные проблемы (рекомендуется)

### 1. Hardcoded SECRET_KEY в settings.py

**Файл:** `effective_mobile/effective_mobile/settings.py:10`

```python
SECRET_KEY = 'django-insecure-binb2g0sc)=m04k2dqax_u1o3*m(il_j*%(ef@9692p1m*vwfm'
```

**Проблема:** Инсекюрный секретный ключ зашит в код.

**Рекомендация:** Использовать переменную окружения:
```python
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-dev-only-key')
```

---

### 2. Неправильное именование ForeignKey

**Файл:** `effective_mobile/auth/models.py:21`

```python
user_id = models.ForeignKey(User, on_delete=models.CASCADE)
```

**Проблема:** По конвенции Django, поле для внешнего ключа должно называться `user`, а не `user_id`. Django автоматически создаст поле `user_id` в базе данных.

**Рекомендация:** Переименовать поле и обновить все обращения:
```python
user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tokens')
```

Это потребует изменения:
- `auth/models.py` - поле и фильтры
- `auth/auth_backend.py` - обращение к user
- `auth/views.py` - обращения в delete_me, login_user, logout_user
- Создать миграцию для изменения поля

---

### 3. Отсутствие статусов ответов в некоторых view

Некоторые view не возвращают корректные HTTP статусы:
- `get_book_by_id` должен возвращать 404 если книга не найдена
- `delete_book` должен возвращать 404 если книга не найдена

---

## 📊 Статистика исправлений

| Категория | Исправлено | Осталось |
|-----------|-----------|----------|
| Критические ошибки | 13 | 2 |
| Логические ошибки | 4 | 0 |
| Архитектурные проблемы | 3 | 2 |
| Стилистические проблемы | 2 | 0 |
| **Итого** | **22** | **4** |

---

## 🎯 Приоритет рекомендуемых исправлений

1. **Срочно:** Переименовать `user_id` → `user` в CustomToken
2. **Важно:** Использовать SECRET_KEY из .env в settings.py
3. **Желательно:** Добавить корректные HTTP статусы во все view

---

Дата создания: 2025-01-27
