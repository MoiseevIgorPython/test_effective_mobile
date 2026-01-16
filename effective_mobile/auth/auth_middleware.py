from django.utils.deprecation import MiddlewareMixin
from .auth_backend import TokenAuthenticationBackend


class TokenAuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]

            backend = TokenAuthenticationBackend()
            user = backend.authenticate(request, token=token)

            if user:
                request.user = user
