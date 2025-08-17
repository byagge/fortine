from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
	path("", views.index, name="index"),
	path("answers/", views.answers, name="answers"),
	path("requests/", views.requests_view, name="requests"),
	path("login/", views.login_view, name="login"),
]
