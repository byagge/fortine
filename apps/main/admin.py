from django.contrib import admin
from .models import FAQ

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
	list_display = ('question', 'is_active', 'order', 'created_at')
	list_editable = ('is_active', 'order')
	search_fields = ('question', 'answer')
	list_filter = ('is_active',)
	ordering = ('order', '-created_at')
	readonly_fields = ('created_at', 'updated_at')
