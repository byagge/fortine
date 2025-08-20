from django.core.management.base import BaseCommand
from apps.config.models import FriendNickname


class Command(BaseCommand):
    help = 'Инициализация начальных настроек сайта'

    def handle(self, *args, **options):
        self.stdout.write('Инициализация настроек сайта...')
        
        # Создаем начальный ник для добавления в друзья
        nickname, created = FriendNickname.objects.get_or_create(
            nickname='@game37op1',
            defaults={
                'platform': 'Fortnite',
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Создан ник: {nickname.nickname}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Ник уже существует: {nickname.nickname}')
            )
        
        self.stdout.write(
            self.style.SUCCESS('Инициализация настроек завершена успешно!')
        ) 