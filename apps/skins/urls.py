from django.urls import path
from . import views

app_name = 'skins'
 
urlpatterns = [
    path('', views.SkinListView.as_view(), name='skin_list'),
    path('<int:pk>/', views.SkinDetailView.as_view(), name='skin_detail'),
] 