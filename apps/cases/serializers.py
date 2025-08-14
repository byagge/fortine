from rest_framework import serializers
from .models import Case, Category
from apps.skins.serializers import SkinSerializer

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ['id', 'name', 'slug']

class CaseSerializer(serializers.ModelSerializer):
	category = CategorySerializer(read_only=True)
	class Meta:
		model = Case
		fields = ['id', 'name', 'image', 'price', 'created_at', 'category']

class CaseDetailSerializer(serializers.ModelSerializer):
	skins = SkinSerializer(many=True, read_only=True)
	category = CategorySerializer(read_only=True)
	
	class Meta:
		model = Case
		fields = ['id', 'name', 'image', 'price', 'created_at', 'category', 'skins'] 