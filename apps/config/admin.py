from django.contrib import admin
from django.utils.html import format_html
from .models import SiteConfig, FriendNickname


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ['key', 'value_preview', 'description_preview', 'updated_at']
    list_filter = ['updated_at']
    search_fields = ['key', 'value', 'description']
    readonly_fields = ['updated_at']
    ordering = ['key']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('key', 'value', 'description')
        }),
        ('Системная информация', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )
    
    def value_preview(self, obj):
        """Предварительный просмотр значения"""
        if len(obj.value) > 50:
            return format_html('<span title="{}">{}</span>', obj.value, obj.value[:50] + '...')
        return obj.value
    value_preview.short_description = 'Значение'
    
    def description_preview(self, obj):
        """Предварительный просмотр описания"""
        if obj.description and len(obj.description) > 30:
            return format_html('<span title="{}">{}</span>', obj.description, obj.description[:30] + '...')
        return obj.description or '-'
    description_preview.short_description = 'Описание'


@admin.register(FriendNickname)
class FriendNicknameAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'platform', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'platform', 'created_at', 'updated_at']
    search_fields = ['nickname', 'platform']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-is_active', '-updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('nickname', 'platform', 'is_active')
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['activate_nicknames', 'deactivate_nicknames']
    
    def activate_nicknames(self, request, queryset):
        """Активировать выбранные ники"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'Активировано {updated} ников.')
    activate_nicknames.short_description = 'Активировать выбранные ники'
    
    def deactivate_nicknames(self, request, queryset):
        """Деактивировать выбранные ники"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'Деактивировано {updated} ников.')
    deactivate_nicknames.short_description = 'Деактивировать выбранные ники'
    
    def save_model(self, request, obj, form, change):
        """При сохранении модели"""
        if obj.is_active:
            # Деактивируем все остальные ники, если текущий активен
            FriendNickname.objects.exclude(pk=obj.pk).update(is_active=False)
        super().save_model(request, obj, form, change)
