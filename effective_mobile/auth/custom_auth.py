from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser
from .models import CustomToken, User


class CustomTokenAuthentication(BaseAuthentication):
    """
    Аутентификация по кастомному токену.
    Токен должен передаваться в заголовке:
    Authorization: Bearer <токен>
    """

    def authenticate(self, request):
        # 1. Получаем заголовок Authorization
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')

        if not auth_header:
            return None

        parts = auth_header.split()

        if len(parts) != 2:
            raise AuthenticationFailed('Неверный формат заголовка Authorization. '
                                       'Ожидается: Bearer <token>')

        if parts[0].lower() != 'bearer':
            raise AuthenticationFailed('Неверная схема аутентификации. '
                                       'Используйте Bearer токен')

        token = parts[1]

        try:
            custom_token = CustomToken.objects.select_related('user_id').get(token=token)
            if hasattr(custom_token, 'is_valid'):
                if not custom_token.is_valid():
                    raise AuthenticationFailed('Токен просрочен')
            return (custom_token.user_id, custom_token)

        except CustomToken.DoesNotExist:
            raise AuthenticationFailed('Недействительный токен')

    def authenticate_header(self, request):
        """
        Возвращает строку для заголовка WWW-Authenticate.
        DRF использует это для ответов 401 Unauthorized.
        """
        return 'Bearer realm="api"'