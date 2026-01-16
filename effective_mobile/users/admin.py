from django.contrib import admin

from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email',
                    'username',
                    'name',
                    'surname',
                    'fathername',
                    'role')

    fieldsets = (
        (None, {'fields':
                ('email', 'username')}),
        ('Персональная информация', {'fields':
                                     ('name', 'surname', 'fathername', 'role')}),
        ('Права доступа', {'fields':
                           ('is_active', 'is_staff', 'is_superuser')}))
