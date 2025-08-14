from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'cases', api_views.CaseViewSet)
router.register(r'categories', api_views.CategoryViewSet)

app_name = 'cases_api'

urlpatterns = [
	path('', include(router.urls)),
] 