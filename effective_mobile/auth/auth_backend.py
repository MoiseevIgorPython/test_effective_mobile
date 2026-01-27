from django.contrib.auth import backends, get_user_model

from .models import CustomToken

User = get_user_model()


class TokenAuthenticationBackend(backends.BaseBackend):
    """Бэкенд аутентификации."""

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
