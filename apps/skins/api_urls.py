from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'skins', api_views.SkinViewSet)
router.register(r'wins', api_views.AdminWinsViewSet, basename='wins')

app_name = 'skins_api'

urlpatterns = [
	path('', include(router.urls)),
] 