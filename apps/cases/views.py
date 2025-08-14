from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from .models import Case

# Create your views here.

class CaseListView(ListView):
    model = Case
    template_name = 'cases/case_list.html'
    context_object_name = 'cases'
    paginate_by = 12

class CaseDetailView(DetailView):
    model = Case
    template_name = 'cases/case_detail.html'
    context_object_name = 'case'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем скины для этого кейса, отсортированные по шансу выпадения
        context['skins'] = self.object.skins.all().order_by('-drop_chance')
        return context

def opencase_view(request):
    """Представление для шаблона opencase.html"""
    case_id = request.GET.get('case_id')
    
    if case_id:
        try:
            case = Case.objects.get(id=case_id)
            skins = case.skins.all().order_by('-drop_chance')
        except Case.DoesNotExist:
            case = None
            skins = []
    else:
        # Если ID не указан, берем первый доступный кейс
        try:
            case = Case.objects.first()
            skins = case.skins.all().order_by('-drop_chance') if case else []
        except:
            case = None
            skins = []
    
    return render(request, 'cases/opencase.html', {
        'case': case,
        'skins': skins
    })

def scrollcase_view(request):
    """Представление для шаблона scrollcase.html"""
    case_id = request.GET.get('case_id')
    
    if case_id:
        try:
            case = Case.objects.get(id=case_id)
            skins = case.skins.all().order_by('-drop_chance')
        except Case.DoesNotExist:
            case = None
            skins = []
    else:
        # Если ID не указан, берем первый доступный кейс
        try:
            case = Case.objects.first()
            skins = case.skins.all().order_by('-drop_chance') if case else []
        except:
            case = None
            skins = []
    
    return render(request, 'cases/scrollcase.html', {
        'case': case,
        'skins': skins
    })

def api_test_view(request):
    """Представление для тестирования API"""
    return render(request, 'cases/api_test.html')
