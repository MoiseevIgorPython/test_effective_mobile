from rest_framework import serializers
from django.contrib.auth import get_user_model

from books.models import Books

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор моделю пользователя."""

    class Meta:
        model = User
        fields = '__all__'


class CreateUserSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации нового пользователя."""

    repeat_password = serializers.CharField()

    class Meta:
        model = User
        fields = ['name',
                  'username',
                  'surname',
                  'fathername',
                  'email',
                  'password',
                  'repeat_password']

    def validate(self, attrs):
        password = attrs.get("password")
        repeat_password = attrs.get("repeat_password")
        if password != repeat_password:
            raise serializers.ValidationError("Пароли не совпадают.")
        return attrs


class UpdateUserSerializer(serializers.ModelSerializer):
    """Сериализатор изменения пользователя."""

    class Meta:
        model = User
        fields = [
            'name',
            'username',
            'surname',
            'fathername',
            'email'
        ]


class BookSerializer(serializers.ModelSerializer):
    """Сериализатор модели Book."""

    class Meta:
        model = Books
        fields = [
            'title',
            'description',
            'is_published',
            'author'
        ]


class CreateBookSerializer(serializers.ModelSerializer):
    """Сериализатор создания книги."""

    class Meta:
        model = Books
        fields = [
            'title',
            'description',
            'author_id'
        ]
