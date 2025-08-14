from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import Case, Category
from .serializers import CaseSerializer, CaseDetailSerializer
from apps.skins.models import UserSkin  # record user wins
from .serializers import CategorySerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = Category.objects.prefetch_related('cases').all()
	serializer_class = CategorySerializer
	permission_classes = [AllowAny]

class CaseViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = Case.objects.all()
	serializer_class = CaseSerializer
	permission_classes = [AllowAny]
	
	def get_serializer_class(self):
		if self.action == 'retrieve':
			return CaseDetailSerializer
		return CaseSerializer
	
	def get_permissions(self):
		# Разрешаем всем читать список/детали/скины; открытие кейса только авторизованным
		if self.action in ['list', 'retrieve', 'skins']:
			return [AllowAny()]
		if self.action == 'open':
			return [IsAuthenticated()]
		return super().get_permissions()
	
	@action(detail=True, methods=['get'])
	def skins(self, request, pk=None):
		"""Получить все скины для конкретного кейса"""
		case = self.get_object()
		skins = case.skins.all().order_by('-drop_chance')
		from apps.skins.serializers import SkinSerializer
		serializer = SkinSerializer(skins, many=True)
		return Response(serializer.data)
	
	@action(detail=True, methods=['post'])
	def open(self, request, pk=None):
		"""Открыть кейс и получить случайный скин"""
		case = self.get_object()
		
		# Проверяем, есть ли скины в кейсе
		if not case.skins.exists():
			return Response(
				{'error': 'В этом кейсе нет скинов'}, 
				status=status.HTTP_400_BAD_REQUEST
			)
		
		# Получаем случайный скин на основе шансов выпадения
		import random
		
		# Создаем список скинов с учетом их шансов
		skins_with_weights = []
		for skin in case.skins.all():
			# Умножаем шанс на 10000 для более точного расчета
			weight = int(float(skin.drop_chance) * 10000)
			skins_with_weights.extend([skin] * max(1, weight))
		
		if not skins_with_weights:
			return Response(
				{'error': 'Ошибка расчета шансов'}, 
				status=status.HTTP_500_INTERNAL_SERVER_ERROR
			)
		
		# Выбираем случайный скин
		won_skin = random.choice(skins_with_weights)
		
		# Списываем стоимость кейса
		profile = request.user.profile
		if not profile.subtract_balance(case.price):
			return Response({'success': False, 'error': 'Недостаточно средств на балансе'}, status=status.HTTP_400_BAD_REQUEST)
		
		# Записываем выигрыш
		UserSkin.objects.create(user=request.user, skin=won_skin, case=case)
		
		# Сериализуем выигранный скин
		from apps.skins.serializers import SkinDropSerializer
		serializer = SkinDropSerializer(won_skin)
		
		return Response({
			'success': True,
			'message': 'Поздравляем! Вы выиграли скин!',
			'skin': serializer.data,
			'case_name': case.name,
			'balance': str(profile.balance)
		}) 