from django.contrib.auth import authenticate, get_user_model, login, logout
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.serializers import CreateUserSerializer, UpdateUserSerializer, UserSerializer
from auth.models import CustomToken

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, email=email, password=password)
    if user and user.is_active:
        new_token = CustomToken.generate_token(user)
        return Response({'token': new_token.token,
                         'user_id': user.id},
                        status=status.HTTP_201_CREATED)
    return Response({"message": "Пользователь не найден"},
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def registration(request):
    """Регистрация нового пользователя."""
    data = request.data
    serializer = CreateUserSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        validated_data = serializer.validated_data
        email = validated_data['email']
        username = validated_data['username']
        password = validated_data['password']
        new_user = User.objects.create_user(email=email,
                                            username=username,
                                            password=password)
        return Response({
                    'message': 'Пользователь успешно зарегистрирован',
                    'user': {'id': new_user.id,
                             'email': new_user.email,
                             'username': new_user.username}},
                        status=status.HTTP_201_CREATED)
    return Response({"message": "Не верные данные."},
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_me(request):
    """Запрос данных о своем аккаунте."""
    if request.user.is_authenticated:
        user = UserSerializer(request.user)
        return Response({"my_profile": {"name": user.data['name'],
                                        "surname": user.data['surname'],
                                        "fathername": user.data['fathername'],
                                        "username": user.data['username']}},
                        status=status.HTTP_200_OK)
    return Response({"message": "Вы не аутентифицированы"})


@api_view(['GET'])
def update_me(request):
    user = request.user
    serializer = UpdateUserSerializer(
        instance=user,
        data=request.data,
        partial=True)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response({'message': 'Данные успешно обновлены',
                         'user': serializer.data},
                        status=status.HTTP_200_OK)
    return Response({'message': 'Ошибка валидации'},
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def delete_me(request):
    user = request.user
    user.is_active = False
    user.save()
    CustomToken.objects.filter(user_id=user).delete()
    logout(request)
    return Response({"message": "Вы удалены (Ваш объект User не активен)"})


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, email=email, password=password)
    if user is not None and user.is_active:
        login(request, user)
        return Response(data={"message": "Вы аутентифицированы",
                              "user": {"username": user.username,
                                       "email": user.email,
                                       "name": user.name}},
                        status=status.HTTP_200_OK)
    return Response({"message": "Пользователь не найден или неактивен"},
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def logout_user(request):
    CustomToken.objects.filter(user_id=request.user).delete()
    logout(request)
    return Response({"message": "Вы вышли из системы."})



















# // {   
# //     "email": "igor@ya.ru",
# //     "name": "igor",
# //     "surname": "moiseev",
# //     "fathername": "maximich",
# //     "password": "igor12345",
# //     "repeat_password": "igor12345"
# // }

# // {
# //     "username": "igormoiseev",
# //     "password": "igor12345"
# // }