# test_effective_mobile
Тестовое задание - разработка кастомного механизма аутентификации и авторизации

Автор Моисеев Игорь ТГ: @igormaximich


Задание показалось достаточно тяжелым но было очень интересно, требуется дальнейшее изучение механизма автоматической авторизации (проверки токена переданного в заголовке).
Старался максимально кастомизировать данное приложение.
В своей реализации я проверял наличие в таблице CustomToken объекта соответствующего тегущему пользователю, хоть и хранить токен в базе не является корректным.

1. Приложение состоит из нескольких частей:
```text
test_effective_mobile/
├── effective_mobile/
│   ├── api/
│   │   ├── permissions.py        # кастомные пермишины
│   │   ├── serializers.py        # сериализаторы
│   │   ├── urls.py
│   │   └── ...
│   ├── auth/
│   │   ├── auth_backend.py  # бэкенд аутентификации
│   │   ├── auth_middleware.py
│   │   ├── models.py        # Модель Токена
│   │   ├── urls.py          # urls обработки запросов к User
│   │   └── views.py         # обработчики запросов (регистрация, логин, логаут и т д)
│   ├── users/
│   │   ├── models.py        # Кастомная модель User
│   │   └── ...
│   ├── books/
│   │   ├── models.py        # Модель Book
│   │   ├── urls.py          # urls бработки запросов к Book
│   │   ├── views.py         # обработчики запросов для книг
│   │   └── ...
│   ├── effective_mobile/    # Настройки проекта, базовые urls
│   └── manage.py
├── .env.example             # Шаблон переменных окружения
├── requirements.txt         # Зависимости Python
└── README.md
```

2. Разграничение прав осуществляется путем описания пермишинов основанных на классе rest_framework.permissions.BasePermissions

В свою очередь у пользователей есть атрибут role, принимающий значение USER, MODERATOR или ADMIN
В пермишнах проверяется является ли текущий пользователь ADMIN, MODERATOR или являетсля ли он автором объекта модели Books.

3. Изменять роли, редактировать/добавлять/удалять объекты User и Book можно через админ-панель доступную по адресу

```
127.0.0.1:8000/admin
```

4. Развертывание приложения:

Клонирование репозитория:
```
git clone git@github.com:MoiseevIgorPython/test_effective_mobile.git
cd test_effective_mobile
```

Создание виртуального окружения:
```
python -m venv venv
. venv/bin/activate  # для Linux/Mac
# или
. venv/Scripts/activate     # для Windows
```

Установка зависимостей:

```
pip install -r requirements.txt
```

Настройка окружения:

# Отредактируйте .env файл, указав свои настройки БД (пример в файле .env.example)

Выполнить миграции:
```
python manage.py makemigrations
python manage.py migrate
```

Добавить тестовые данные

```
python manage.py add_test_objects
```