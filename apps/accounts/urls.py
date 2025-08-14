from django.urls import path
from . import views
from apps.main import views as main_views

urlpatterns = [
    path("csrf/", views.get_csrf_token, name="accounts_csrf"),
    path("login-or-register/", views.LoginOrRegisterView.as_view(), name="login_or_register"),
    path("account-info/", views.AccountInfoView.as_view(), name="account_info"),
    path("update-profile/", views.UpdateProfileView.as_view(), name="update_profile"),
    path("upload-avatar/", views.UploadAvatarView.as_view(), name="upload_avatar"),
    path("logout/", views.logout_user, name="logout"),
    path("user-skins/", views.get_user_skins, name="user_skins"),
    path("", main_views.account, name="account"),
] 