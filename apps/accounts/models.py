from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Баланс")
	avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Аватар")
	# Added back optional profile fields used by views/UI
	PLATFORM_CHOICES = [
		('playstation', 'PlayStation'),
		('xbox', 'Xbox'),
		('nintendo', 'Nintendo'),
		('apple', 'Apple'),
		('windows', 'Windows'),
		('android', 'Android'),
	]
	nick_in_game = models.CharField(max_length=100, blank=True, verbose_name="Ник в игре")
	platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, blank=True, verbose_name="Платформа")
	created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
	updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

	class Meta:
		verbose_name = "Профиль пользователя"
		verbose_name_plural = "Профили пользователей"

	def __str__(self):
		return f"Профиль {self.user.username}"

	def add_balance(self, amount):
		"""Добавить средства к балансу"""
		self.balance += amount
		self.save()

	def subtract_balance(self, amount):
		"""Списать средства с баланса"""
		if self.balance >= amount:
			self.balance -= amount
			self.save()
			return True
		return False
