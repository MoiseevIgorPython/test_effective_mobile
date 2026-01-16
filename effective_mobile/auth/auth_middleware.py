from django.utils.deprecation import MiddlewareMixin
from .auth_backend import TokenAuthenticationBackend


class TokenAuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # # Пропускаем аутентификацию для некоторых путей
        # if request.path.startswith('/admin/'):
        #     return

        # Получаем токен из заголовка
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]  # Убираем 'Bearer '

            backend = TokenAuthenticationBackend()
            user = backend.authenticate(request, token=token)

            if user:
                request.user = user
