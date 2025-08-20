from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import FriendNickname


@api_view(['GET'])
def get_active_nickname(request):
    """Получить активный ник для добавления в друзья"""
    try:
        nickname_obj = FriendNickname.get_active_nickname()
        if nickname_obj:
            return Response({
                'nickname': nickname_obj.nickname,
                'platform': nickname_obj.platform,
                'is_active': nickname_obj.is_active
            })
        else:
            return Response({
                'nickname': '@game37op1',  # Значение по умолчанию
                'platform': '',
                'is_active': False
            })
    except Exception as e:
        return Response({
            'error': 'Ошибка при получении ника',
            'nickname': '@game37op1'  # Fallback значение
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 