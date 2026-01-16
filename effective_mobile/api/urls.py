from django.urls import include, path

urlpatterns = [
    path('user/', include('auth.urls')),
    path('books/', include('books.urls'))
]
