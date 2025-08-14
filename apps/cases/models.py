from django.db import models

# Create your models here.

class Category(models.Model):
	name = models.CharField(max_length=255, unique=True, verbose_name="Категория")
	slug = models.SlugField(max_length=255, unique=True, verbose_name="Слаг")
	order = models.IntegerField(default=0, verbose_name="Порядок")
	created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
	updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

	class Meta:
		verbose_name = "Категория кейсов"
		verbose_name_plural = "Категории кейсов"
		ordering = ['order', 'name']

	def __str__(self):
		return self.name

class Case(models.Model):
	name = models.CharField(max_length=255, verbose_name="Название кейса")
	image = models.ImageField(upload_to='cases/', verbose_name="Фото кейса")
	price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
	created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
	updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='cases', verbose_name="Категория")

	class Meta:
		verbose_name = "Кейс"
		verbose_name_plural = "Кейсы"
		ordering = ['-created_at']

	def __str__(self):
		return self.name
