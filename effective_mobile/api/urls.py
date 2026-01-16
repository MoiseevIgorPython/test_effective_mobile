from django.urls import path, include


urlpatterns = [
    path('user/', include('auth.urls')),
    path('books/', include('books.urls'))
]
