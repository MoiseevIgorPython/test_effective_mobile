from rest_framework.permissions import BasePermission

from books.models import Books
from users.models import CustomUser


class OnlyAuthor(BasePermission):
    """Доступ владельцу."""

    def has_permission(self, request, view):
        if request.method == 'GET':
            book_id = request.parser_context.get('kwargs', {}).get('book_id')
            if not book_id:
                return False
            book = Books.objects.get(id=book_id, is_published=True)
            return book.author_id == request.user.id
        return False


class OnlyModeratorOrAdmin(BasePermission):
    """Доступ администраторам и модераторам."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.role in [CustomUser.ADMIN,
                                          CustomUser.MODERATOR])
