from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Skin

# Create your views here.

class SkinListView(ListView):
    model = Skin
    template_name = 'skins/skin_list.html'
    context_object_name = 'skins'
    paginate_by = 20

    def get_queryset(self):
        queryset = Skin.objects.select_related('case').all()
        # Фильтрация по кейсу
        case_id = self.request.GET.get('case')
        if case_id:
            queryset = queryset.filter(case_id=case_id)
        # Фильтрация по редкости
        rarity = self.request.GET.get('rarity')
        if rarity:
            queryset = queryset.filter(rarity=rarity)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from apps.cases.models import Case
        context['cases'] = Case.objects.all()
        context['rarity_choices'] = Skin._meta.get_field('rarity').choices
        return context

class SkinDetailView(DetailView):
    model = Skin
    template_name = 'skins/skin_detail.html'
    context_object_name = 'skin'
