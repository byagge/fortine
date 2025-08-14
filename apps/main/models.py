from django.db import models

# Create your models here.

class FAQ(models.Model):
	question = models.CharField(max_length=300, verbose_name="Вопрос")
	answer = models.TextField(verbose_name="Ответ")
	order = models.IntegerField(default=0, verbose_name="Порядок")
	is_active = models.BooleanField(default=True, verbose_name="Активен")
	created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
	updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

	class Meta:
		verbose_name = "FAQ вопрос"
		verbose_name_plural = "FAQ вопросы"
		ordering = ['order', '-created_at']

	def __str__(self) -> str:
		return self.question
