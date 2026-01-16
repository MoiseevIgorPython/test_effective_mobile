from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (AbstractBaseUser,
                                        PermissionsMixin,
                                        BaseUserManager)


class CustomUserManager(BaseUserManager):
    def create_user(self,
                    email,
                    username,
                    password=None,
                    **extra_fields):
        """Создает и сохраняет обычного пользователя."""

        if not email:
            raise ValueError('Email обязателен')
        if not username:
            raise ValueError('Имя пользователя обязательно')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,
                         email,
                         username,
                         password=None,
                         **extra_fields):
        """Создает и сохраняет суперпользователя."""

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', self.model.ADMIN)

        return self.create_user(email,
                                username,
                                password,
                                **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Кастомная модель пользователя."""

    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

    ROLE_CHOICES = [(USER, 'user'),
                    (MODERATOR, 'moderator'),
                    (ADMIN, 'admin')]

    name = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)
    fathername = models.CharField(max_length=32)
    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(max_length=150, unique=True)
    role = models.CharField(choices=ROLE_CHOICES,
                            default=USER)

    USERNAME_FIELD = 'email'        # Поле для входа (логин)
    REQUIRED_FIELDS = ['username']  # Поля для createsuperuser

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True
