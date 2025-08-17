from django.urls import path
from . import views

urlpatterns = [
	path("", views.index, name="index"),
	path("answers/", views.answers, name="answers"),
	path("requests/", views.requests_view, name="requests"),
	path("login/", views.login_view, name="login"),
]
