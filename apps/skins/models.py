from django.db import models
from apps.cases.models import Case
from django.contrib.auth import get_user_model

class Skin(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='skins', verbose_name="Кейс")
    name = models.CharField(max_length=255, verbose_name="Название скина")
    image = models.ImageField(upload_to='skins/', verbose_name="Фото скина")
    drop_chance = models.DecimalField(max_digits=5, decimal_places=4, verbose_name="Шанс выпадения", 
                                    help_text="Шанс в диапазоне от 0.0001 до 1.0000")
    rarity = models.CharField(max_length=50, choices=[
        ('common', 'Обычный'),
        ('uncommon', 'Необычный'),
        ('rare', 'Редкий'),
        ('epic', 'Эпический'),
        ('legendary', 'Легендарный'),
    ], default='common', verbose_name="Редкость")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Скин"
        verbose_name_plural = "Скины"
        ordering = ['case', '-drop_chance']

    def __str__(self):
        return f"{self.name} ({self.case.name})"

    def get_drop_percentage(self):
        """Возвращает шанс выпадения в процентах"""
        return float(self.drop_chance) * 100

# New model to store user wins
User = get_user_model()

class UserSkin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='won_skins', verbose_name="Пользователь")
    skin = models.ForeignKey(Skin, on_delete=models.CASCADE, related_name='user_wins', verbose_name="Скин")
    case = models.ForeignKey(Case, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_wins', verbose_name="Кейс")
    won_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата выигрыша")
    status = models.CharField(max_length=20, choices=[('pending', 'В ожидании'), ('delivered', 'Доставлено')], default='pending', verbose_name="Статус")

    class Meta:
        verbose_name = "Скин пользователя"
        verbose_name_plural = "Скины пользователя"
        ordering = ['-won_at']

    def __str__(self):
        return f"{self.user.username} — {self.skin.name} ({self.case.name if self.case else '-'})"
