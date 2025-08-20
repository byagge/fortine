from django.urls import path
from . import api_views

app_name = 'config_api'

urlpatterns = [
    path('nickname/', api_views.get_active_nickname, name='get_active_nickname'),
] 