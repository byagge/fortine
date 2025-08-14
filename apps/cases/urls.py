from django.urls import path
from . import views

app_name = 'cases'

urlpatterns = [
    path('', views.CaseListView.as_view(), name='case_list'),
    path('<int:pk>/', views.CaseDetailView.as_view(), name='case_detail'),
    path('opencase/', views.opencase_view, name='opencase'),
    path('scrollcase/', views.scrollcase_view, name='scrollcase'),
    path('api-test/', views.api_test_view, name='api_test'),
] 