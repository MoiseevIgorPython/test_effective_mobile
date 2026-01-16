from django.urls import path

from . import views

urlpatterns = [
    path('auth/', views.get_token),             # получить токен
    path('registration/', views.registration),  # регистрация
    path('me/', views.get_me),         # получение данных залогиненного пользователя
    path('update/', views.update_me),  # редактирование данных
    path('delete/', views.delete_me),  # удаление пользователя
    path('login/', views.login_user),       # вход в систему
    path('logout/', views.logout_user),     # выход из системы
]
