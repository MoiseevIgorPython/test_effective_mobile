from django.contrib import admin

from books.models import Books


@admin.register(Books)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title',
                    'description',
                    'author',
                    'is_published')