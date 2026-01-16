from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from api.permissions import OnlyAuthor, OnlyModeratorOrAdmin
from books.models import Books
from api.serializers import BookSerializer, CreateBookSerializer
from rest_framework.permissions import IsAuthenticated


User = get_user_model()


@api_view(['GET'])
@permission_classes([OnlyModeratorOrAdmin])       # только админы
def get_all_books(request):
    books = Books.objects.all()                   # админы получают все книги, в том числе не опубликованные
    serializer = BookSerializer(books, many=True)
    return Response({"books": serializer.data})


@api_view(['GET'])
@permission_classes([IsAuthenticated, OnlyAuthor])   # только аутентифицированные владельцы книги
def get_my_books(request):
    user = request.user
    books = Books.objects.filter(author_id=user.id,
                                 is_published=True)  # владелец получает только опубликованные книги
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, OnlyAuthor])   # только аутентифицированные владельцы книги
def get_book_by_id(request, book_id):
    book = Books.objects.filter(id=book_id,
                                is_published=True).first()
    if book:
        return Response({"book": {"title": book.title,
                                  "description": book.description}})
    return Response({"message": "Книга не найдена."})


@api_view(['GET'])
@permission_classes([OnlyAuthor, OnlyModeratorOrAdmin])  # только владельцы данной книги (~IsAuthenticated)
def delete_book(request, book_id):
    book = Books.objects.filter(id=book_id).first()
    if book:
        book.delete()
        return Response({"message": "Книга удалена."})
    return Response({"message": "Книга не найдена."})


@api_view(['GET'])          # по умолчанию IsAuthenticated
def create_book(request):
    data = request.data
    user = request.user
    data['author_id'] = user.id
    serializer = CreateBookSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        new_book = Books.objects.create(**data)
        return Response({"message": "Книга создана.",
                         "new_book": new_book.title})
    return Response({"message": "Не валидные данные."})
