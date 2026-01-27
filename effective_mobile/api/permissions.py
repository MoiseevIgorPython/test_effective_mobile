from rest_framework.permissions import BasePermission

from books.models import Books
from users.models import CustomUser


class OnlyAuthor(BasePermission):
    """Доступ владельцу."""

    def has_permission(self, request, view):
        book_id = request.parser_context.get('kwargs', {}).get('book_id')
        if not book_id:
            return True
        try:
            book = Books.objects.get(id=book_id)
        except Books.DoesNotExist:
            return False
        return book.author == request.user

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class OnlyModeratorOrAdmin(BasePermission):
    """Доступ администраторам и модераторам."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.role in [CustomUser.ADMIN,
                                          CustomUser.MODERATOR])
