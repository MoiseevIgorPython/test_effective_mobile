import os

import jwt
from django.contrib.auth import get_user_model
from django.db import models
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY', 'my_secret_key')
ALGORITHM = os.getenv('ALGORITHM', '')


User = get_user_model()


class CustomToken(models.Model):
    """Модель токена."""

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)

    @classmethod
    def generate_token(cls, user):
        cls.objects.filter(user_id=user).delete()  # при генерации нового токена удаляем старый

        payload = {"sub": str(user.id),
                   "user_id": user.id}                # на время разработки токен бессрочный
        new_token = jwt.encode(
            payload=payload,
            key=SECRET_KEY,
            algorithm=ALGORITHM)
        return cls.objects.create(user_id=user,
                                  token=new_token)
