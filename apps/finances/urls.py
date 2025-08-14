from django.urls import path
from . import views

app_name = 'finances'

urlpatterns = [
	path('deposit/', views.deposit_view, name='deposit'),
	path('history/', views.history_view, name='history'),
] 