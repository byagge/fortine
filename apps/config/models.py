from django.db import models

# Create your models here.


class SiteConfig(models.Model):
    """Модель для хранения настраиваемых параметров сайта"""
    
    key = models.CharField(max_length=100, unique=True, verbose_name="Ключ параметра")
    value = models.TextField(verbose_name="Значение")
    description = models.TextField(blank=True, verbose_name="Описание")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Настройка сайта"
        verbose_name_plural = "Настройки сайта"
        ordering = ['key']
    
    def __str__(self):
        return f"{self.key}: {self.value}"
    
    @classmethod
    def get_value(cls, key, default=None):
        """Получить значение параметра по ключу"""
        try:
            config = cls.objects.get(key=key)
            return config.value
        except cls.DoesNotExist:
            return default
    
    @classmethod
    def set_value(cls, key, value, description=""):
        """Установить значение параметра"""
        config, created = cls.objects.get_or_create(
            key=key,
            defaults={'value': value, 'description': description}
        )
        if not created:
            config.value = value
            config.description = description
            config.save()
        return config


class FriendNickname(models.Model):
    """Модель для хранения ника для добавления в друзья"""
    
    nickname = models.CharField(max_length=100, verbose_name="Ник для добавления в друзья")
    platform = models.CharField(max_length=50, blank=True, verbose_name="Платформа")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Ник для добавления в друзья"
        verbose_name_plural = "Ники для добавления в друзья"
        ordering = ['-is_active', '-updated_at']
    
    def __str__(self):
        return f"{self.nickname} ({self.platform})"
    
    @classmethod
    def get_active_nickname(cls):
        """Получить активный ник для добавления в друзья"""
        try:
            return cls.objects.filter(is_active=True).first()
        except:
            return None
