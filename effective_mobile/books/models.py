from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Books(models.Model):
    """Класс объектов Books связанных с Users."""

    title = models.CharField(max_length=32)
    description = models.CharField(max_length=256, default="")
    is_published = models.BooleanField(default=True)
    author = models.ForeignKey(User,
                               related_name='books',
                               on_delete=models.CASCADE)
