from django.core.management.base import BaseCommand

from books.models import Books
from users.models import CustomUser


class Command(BaseCommand):
    help = 'Создает тестовых пользователей и книги'

    def handle(self, *args, **options):
        user1 = CustomUser.objects.create_user(
            email='user1@example.com',
            username='user1',
            password='password123',
            name='Иван',
            surname='Петров',
            fathername='Иванович',
            role='user')

        user2 = CustomUser.objects.create_user(
            email='user2@example.com',
            username='user2',
            password='password123',
            name='Мария',
            surname='Сидорова',
            fathername='',
            role='user')

        moderator = CustomUser.objects.create_user(
            email='moderator@example.com',
            username='moderator',
            password='password123',
            name='Алексей',
            surname='Смирнов',
            fathername='Петрович',
            role='moderator')

        test_admin = CustomUser.objects.create_user(
            email='admin@example.com',
            username='admin',
            password='admin',
            surname='Админов',
            fathername='Админович',
            role='admin',
            is_staff=True,
            is_superuser=True)

        books_data = [
            {
                'title': 'Колобок',
                'description': 'Сказка о колобке',
                'author': user1,
                'is_published': True
            },
            {
                'title': 'Чук и Гек',
                'description': 'Приключения Чука и Гека',
                'author': user2,
                'is_published': False
            },
            {
                'title': 'Мастер и Маргарита',
                'description': 'Роман Михаила Булгакова',
                'author': moderator,
                'is_published': True
            }]

        for book_data in books_data:
            Books.objects.create(**book_data)

        self.stdout.write(self.style.SUCCESS('Тестовые данные созданы успешно!'))
        self.stdout.write(f'Создано книг: {Books.objects.count()}')