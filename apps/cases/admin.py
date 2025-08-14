from django.contrib import admin
from .models import Case, Category
from apps.skins.models import Skin

class SkinInline(admin.TabularInline):
    model = Skin
    extra = 1
    fields = ('name', 'image', 'rarity', 'drop_chance')
    
    def has_add_permission(self, request, obj=None):
        """Разрешаем добавление скинов только для существующих кейсов"""
        return obj is not None
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Автоматически устанавливаем кейс для новых скинов"""
        if db_field.name == "case" and obj:
            kwargs["initial"] = obj
            kwargs["disabled"] = True
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'created_at', 'updated_at')
    list_editable = ('order',)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name',)
    ordering = ('order', 'name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'skins_count', 'created_at', 'updated_at')
    list_filter = ('category', 'created_at', 'updated_at')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    inlines = [SkinInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'image', 'price', 'category')
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def skins_count(self, obj):
        return obj.skins.count()
    skins_count.short_description = 'Количество скинов'
    
    def save_formset(self, request, form, formset, change):
        """Сохраняем инлайн-формы и устанавливаем связь с кейсом"""
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, Skin) and not instance.case_id:
                instance.case = form.instance
            instance.save()
        formset.save_m2m()
