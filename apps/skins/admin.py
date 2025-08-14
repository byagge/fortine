from django.contrib import admin
from .models import Skin

@admin.register(Skin)
class SkinAdmin(admin.ModelAdmin):
    list_display = ('name', 'case', 'rarity', 'drop_chance', 'get_drop_percentage_display', 'created_at')
    list_filter = ('case', 'rarity', 'created_at')
    search_fields = ('name', 'case__name')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('case', '-drop_chance')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('case', 'name', 'image', 'rarity')
        }),
        ('Шансы выпадения', {
            'fields': ('drop_chance',),
            'description': 'Введите шанс от 0.0001 до 1.0000'
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_drop_percentage_display(self, obj):
        """Отображает шанс выпадения в процентах"""
        return f"{obj.get_drop_percentage():.2f}%"
    get_drop_percentage_display.short_description = 'Шанс выпадения (%)'
