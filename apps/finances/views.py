from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required


@require_GET
@login_required
def deposit_view(request):
	return render(request, 'deposit.html')


@require_GET
@login_required
def history_view(request):
	# Later we can pass real transactions
	return render(request, 'history.html')
