from rest_framework import serializers
from .models import Skin, UserSkin

class SkinSerializer(serializers.ModelSerializer):
    case_name = serializers.CharField(source='case.name', read_only=True)
    drop_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Skin
        fields = ['id', 'name', 'image', 'rarity', 'drop_chance', 'drop_percentage', 'case_name']
    
    def get_drop_percentage(self, obj):
        return obj.get_drop_percentage()

class SkinDropSerializer(serializers.ModelSerializer):
    """Сериализатор для выпадения скина"""
    case_name = serializers.CharField(source='case.name', read_only=True)
    
    class Meta:
        model = Skin
        fields = ['id', 'name', 'image', 'rarity', 'case_name']

class UserSkinSerializer(serializers.ModelSerializer):
    """Сериализатор для скинов пользователя (победы)."""
    name = serializers.CharField(source='skin.name', read_only=True)
    image = serializers.ImageField(source='skin.image', read_only=True)
    rarity = serializers.CharField(source='skin.rarity', read_only=True)
    case_name = serializers.CharField(source='case.name', read_only=True)
    
    class Meta:
        model = UserSkin
        fields = ['id', 'name', 'image', 'rarity', 'case_name', 'won_at', 'status']

class AdminWinSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    avatar = serializers.SerializerMethodField()
    skin = serializers.CharField(source='skin.name', read_only=True)
    case_name = serializers.CharField(source='case.name', read_only=True)
    date = serializers.DateTimeField(source='won_at', read_only=True)
    
    class Meta:
        model = UserSkin
        fields = ['id', 'user', 'avatar', 'skin', 'case_name', 'date']
    
    def get_avatar(self, obj):
        try:
            prof = obj.user.profile
            return prof.avatar.url if prof.avatar else None
        except Exception:
            return None 