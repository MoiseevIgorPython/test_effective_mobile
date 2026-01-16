from django.contrib.auth import backends, get_user_model

from .models import CustomToken

User = get_user_model()


class TokenAuthenticationBackend(backends.BaseBackend):
    """Бэкенд аутентификации."""

    def authenticate(self, request, token=None):
        if not token:
            return None
        custom_token = CustomToken.objects.get(token=token)
        return custom_token.user

    def get_user(self, user_id):
        return User.objects.get(id=user_id)
