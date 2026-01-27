from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.permissions import OnlyAuthor, OnlyModeratorOrAdmin
from api.serializers import BookSerializer, CreateBookSerializer
from books.models import Books
from users.models import CustomUser

User = get_user_model()


@api_view(['GET'])
@permission_classes([OnlyModeratorOrAdmin])
def get_all_books(request):
    books = Books.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response({"books": serializer.data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_books(request):
    user = request.user
    books = Books.objects.filter(author=user.id,
                                 is_published=True)
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_book_by_id(request, book_id):
    book = get_object_or_404(Books, id=book_id, is_published=True)
    if book.author == request.user:
        return Response({"book": {"title": book.title,
                                  "description": book.description}})
    return Response({"message": "У вас нет прав на просмотр этой книги."},
                    status=status.HTTP_403_FORBIDDEN)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, OnlyAuthor])
def delete_book(request, book_id):
    book = get_object_or_404(Books, id=book_id)
    if book.author == request.user or request.user.role in [CustomUser.ADMIN, CustomUser.MODERATOR]:
        book.delete()
        return Response({"message": "Книга удалена."})
    return Response({"message": "У вас нет прав на удаление этой книги."},
                    status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_book(request):
    serializer = CreateBookSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(author=request.user)
        return Response({"message": "Книга создана.",
                         "new_book": serializer.data['title']},
                        status=status.HTTP_201_CREATED)
    return Response({"message": "Не валидные данные."},
                    status=status.HTTP_400_BAD_REQUEST)
