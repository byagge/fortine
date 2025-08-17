from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


@require_GET
def index(request):
	from apps.cases.models import Case, Category
	featured_cases = Case.objects.select_related('category').all()[:6]  # Показываем первые 6 кейсов
	categories = Category.objects.prefetch_related('cases').all()
	return render(request, "index.html", {
		'featured_cases': featured_cases,
		'categories': categories,
	})


@require_GET
def answers(request):
	from .models import FAQ
	faqs = FAQ.objects.filter(is_active=True).order_by('order', '-created_at')
	return render(request, "answers.html", { 'faqs': faqs })


def account(request):
	return render(request, "account.html")


@require_GET
@staff_member_required
def requests_view(request):
	return render(request, "requests.html")


@require_GET
def login_view(request):
	# Если пользователь уже авторизован, перенаправляем на главную
	if request.user.is_authenticated:
		from django.shortcuts import redirect
		return redirect('index')
	return render(request, "login.html")
