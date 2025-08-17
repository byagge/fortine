from django.contrib.auth import authenticate, login, get_user_model, logout
from django.db import IntegrityError
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from .models import UserProfile
from apps.skins.models import UserSkin

User = get_user_model()


def _generate_unique_username(preferred_username: str) -> str:
	base = preferred_username or "user"
	base = base.strip('@').strip() or "user"
	candidate = base
	suffix = 1
	while User.objects.filter(username=candidate).exists():
		suffix += 1
		candidate = f"{base}{suffix}"
	return candidate


@ensure_csrf_cookie
def get_csrf_token(request):
	token = get_token(request)
	return JsonResponse({"csrfToken": token})


class LoginOrRegisterView(APIView):
	authentication_classes = []  # Allow without prior auth
	permission_classes = []

	def post(self, request: Request) -> Response:
		email = (request.data.get("email") or "").strip().lower()
		password = (request.data.get("password") or "").strip()
		nick_in_game = (request.data.get("name") or "").strip()
		platform = (request.data.get("platform") or "").strip()

		if not email or not password:
			return Response({"success": False, "error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

		# Normalize nickname (keep leading @ in UI but store without it if desired)
		nick_normalized = nick_in_game.lstrip('@')

		# If email or nickname already exists -> treat as login attempt by email
		existing_user_by_email = User.objects.filter(email=email).first()
		existing_user_by_nick = UserProfile.objects.filter(nick_in_game=nick_in_game).first() or UserProfile.objects.filter(nick_in_game=nick_normalized).first()
		if existing_user_by_email or existing_user_by_nick:
			user_for_login = existing_user_by_email or (existing_user_by_nick.user if existing_user_by_nick else None)
			if user_for_login is None:
				return Response({"success": False, "error": "Account exists. Please login."}, status=status.HTTP_400_BAD_REQUEST)
			auth_user = authenticate(request, username=user_for_login.username, password=password)
			if not auth_user:
				return Response({"success": False, "error": "Incorrect password. Email or nickname already taken."}, status=status.HTTP_401_UNAUTHORIZED)
			login(request._request, user_for_login)
			profile = user_for_login.profile
			return Response({
				"success": True,
				"action": "login",
				"user": {
					"id": user_for_login.id,
					"username": user_for_login.username,
					"email": user_for_login.email,
					"nick_in_game": profile.nick_in_game,
					"platform": profile.platform,
					"balance": str(profile.balance),
				},
			})

		# Register new user (email and nickname are free)
		# Ensure nickname is not taken (double-check)
		if UserProfile.objects.filter(nick_in_game=nick_in_game).exists() or UserProfile.objects.filter(nick_in_game=nick_normalized).exists():
			return Response({"success": False, "error": "Nickname already taken. Please login."}, status=status.HTTP_400_BAD_REQUEST)

		username = _generate_unique_username(nick_normalized or email.split("@")[0])
		try:
			new_user = User.objects.create_user(username=username, password=password, email=email)
			# Update profile with provided data (balance defaults to 0)
			profile = new_user.profile
			profile.nick_in_game = nick_in_game or nick_normalized
			if platform in dict(UserProfile.PLATFORM_CHOICES):
				profile.platform = platform
			profile.save()
		except IntegrityError:
			username = _generate_unique_username(nick_normalized or email.split("@")[0])
			new_user = User.objects.create_user(username=username, password=password, email=email)
			profile = new_user.profile
			profile.nick_in_game = nick_in_game or nick_normalized
			if platform in dict(UserProfile.PLATFORM_CHOICES):
				profile.platform = platform
			profile.save()

		login(request._request, new_user)
		return Response({
			"success": True,
			"action": "register",
			"user": {
				"id": new_user.id,
				"username": new_user.username,
				"email": new_user.email,
				"nick_in_game": profile.nick_in_game,
				"platform": profile.platform,
				"balance": str(profile.balance),
			},
		}, status=status.HTTP_201_CREATED)


class AccountInfoView(APIView):
	permission_classes = [IsAuthenticated]
	
	def get(self, request: Request) -> Response:
		"""Получить информацию об аккаунте пользователя"""
		try:
			profile = request.user.profile
			return Response({
				"success": True,
				"user": {
					"id": request.user.id,
					"username": request.user.username,
					"email": request.user.email,
					"nick_in_game": profile.nick_in_game,
					"platform": profile.platform,
					"balance": str(profile.balance),
					"avatar": profile.avatar.url if profile.avatar else None,
					"registration_date": request.user.date_joined.strftime("%d.%m.%Y") if hasattr(request.user, 'date_joined') and request.user.date_joined else None,
				}
			})
		except Exception as e:
			return Response({
				"success": False,
				"error": str(e)
			}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateProfileView(APIView):
	permission_classes = [IsAuthenticated]
	
	def post(self, request: Request) -> Response:
		"""Обновить профиль пользователя"""
		try:
			profile = request.user.profile
			nick_in_game = request.data.get("nick_in_game", "").strip()
			
			if nick_in_game:
				profile.nick_in_game = nick_in_game
				profile.save()
				
				return Response({
					"success": True,
					"message": "Nickname updated successfully",
					"nick_in_game": profile.nick_in_game
				})
			else:
				return Response({
					"success": False,
					"error": "Nickname is required"
				}, status=status.HTTP_400_BAD_REQUEST)
				
		except Exception as e:
			return Response({
				"success": False,
				"error": str(e)
			}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UploadAvatarView(APIView):
	permission_classes = [IsAuthenticated]
	
	def post(self, request: Request) -> Response:
		"""Загрузить аватар пользователя"""
		try:
			if 'avatar' not in request.FILES:
				return Response({
					"success": False,
					"error": "No avatar file provided"
				}, status=status.HTTP_400_BAD_REQUEST)
			
			avatar_file = request.FILES['avatar']
			
			# Проверяем тип файла
			allowed_types = ['image/jpeg', 'image/png', 'image/gif']
			if avatar_file.content_type not in allowed_types:
				return Response({
					"success": False,
					"error": "Invalid file type. Only JPEG, PNG and GIF are allowed."
				}, status=status.HTTP_400_BAD_REQUEST)
			
			# Проверяем размер файла (максимум 5MB)
			if avatar_file.size > 5 * 1024 * 1024:
				return Response({
					"success": False,
					"error": "File too large. Maximum size is 5MB."
				}, status=status.HTTP_400_BAD_REQUEST)
			
			profile = request.user.profile
			
			# Удаляем старый аватар если он существует
			if profile.avatar:
				try:
					if os.path.exists(profile.avatar.path):
						os.remove(profile.avatar.path)
				except:
					pass
			
			# Сохраняем новый аватар
			profile.avatar = avatar_file
			profile.save()
			
			return Response({
				"success": True,
				"message": "Avatar uploaded successfully",
				"avatar_url": profile.avatar.url
			})
			
		except Exception as e:
			return Response({
				"success": False,
				"error": str(e)
			}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
	"""Выйти из аккаунта"""
	try:
		logout(request._request)
		return Response({
			"success": True,
			"message": "Logged out successfully"
		})
	except Exception as e:
		return Response({
			"success": False,
			"error": str(e)
		}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_skins(request):
	"""Получить скины пользователя"""
	wins = UserSkin.objects.filter(user=request.user).select_related('skin', 'case').order_by('-won_at')
	data = []
	for win in wins:
		data.append({
			"id": win.id,
			"name": win.skin.name,
			"case_name": win.case.name if win.case else None,
			"rarity": win.skin.rarity,
			"image": win.skin.image.url if win.skin.image else None,
			"won_at": win.won_at.isoformat(),
			"status": win.status,
		})
	return Response({
		"success": True,
		"skins": data
	})
