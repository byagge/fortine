from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters import rest_framework as filters
from django.db.models import Q
from .models import Skin, UserSkin
from .serializers import SkinSerializer, AdminWinSerializer

class SkinFilter(filters.FilterSet):
	case = filters.NumberFilter(field_name='case__id')
	rarity = filters.CharFilter(field_name='rarity')
	
	class Meta:
		model = Skin
		fields = ['case', 'rarity']

class SkinViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = Skin.objects.select_related('case').all()
	serializer_class = SkinSerializer
	permission_classes = [IsAuthenticated]
	filterset_class = SkinFilter
	ordering = ['-drop_chance']
	
	@action(detail=False, methods=['get'])
	def rarities(self, request):
		"""Получить список всех доступных редкостей"""
		rarities = Skin._meta.get_field('rarity').choices
		return Response({
			'rarities': [{'value': value, 'label': label} for value, label in rarities]
		})
	
	@action(detail=False, methods=['get'])
	def by_case(self, request):
		"""Получить скины по ID кейса"""
		case_id = request.query_params.get('case_id')
		if not case_id:
			return Response(
				{'error': 'Необходимо указать case_id'}, 
				status=status.HTTP_400_BAD_REQUEST
			)
		
		skins = self.queryset.filter(case_id=case_id).order_by('-drop_chance')
		serializer = self.get_serializer(skins, many=True)
		return Response(serializer.data)

class AdminWinsViewSet(viewsets.ViewSet):
	permission_classes = [IsAuthenticated, IsAdminUser]
	
	def list(self, request):
		"""Список выигрышей (только для администратора) c фильтрами: from, to, q"""
		qs = UserSkin.objects.select_related('user', 'skin', 'case', 'user__profile').order_by('-won_at')
		from_date = request.query_params.get('from')
		to_date = request.query_params.get('to')
		q = request.query_params.get('q', '').strip()
		if from_date:
			qs = qs.filter(won_at__date__gte=from_date)
		if to_date:
			qs = qs.filter(won_at__date__lte=to_date)
		if q:
			qs = qs.filter(Q(user__username__icontains=q) | Q(skin__name__icontains=q) | Q(case__name__icontains=q))
		# Simple limit (could add pagination)
		qs = qs[:500]
		data = AdminWinSerializer(qs, many=True).data
		return Response({ 'results': data }) 