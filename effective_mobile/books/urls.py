from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_books),
    path('mybooks/', views.get_my_books),
    path('mybooks/create/', views.create_book),
    path('<int:book_id>/', views.get_book_by_id),
    path('<int:book_id>/delete/', views.delete_book)
]
