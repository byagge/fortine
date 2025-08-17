from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from django.shortcuts import render


class HomePage(Page):
    intro = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]


class StaticTemplatePage(Page):
    template_name_override = models.CharField(
        max_length=255, 
        blank=True, 
        help_text="Django template path to render"
    )
    content = RichTextField(blank=True, help_text="Content for the page")
    
    content_panels = Page.content_panels + [
        FieldPanel('template_name_override'),
        FieldPanel('content')
    ]
    
    subpage_types = []
    parent_page_types = ['wagtailcore.Page']
    
    def serve(self, request):
        tpl = (self.template_name_override or '').strip() or None
        if not tpl:
            return super().serve(request)
        return render(request, tpl, {'page': self})


# Dedicated page models for existing site templates
class IndexPage(Page):
    intro = RichTextField(blank=True)
    featured_cases_title = models.CharField(max_length=255, default="Featured Cases")
    
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('featured_cases_title')
    ]
    
    parent_page_types = ['wagtailcore.Page']
    subpage_types = []
    
    def serve(self, request):
        from apps.cases.models import Case, Category
        featured_cases = Case.objects.select_related('category').all()[:6]
        categories = Category.objects.prefetch_related('cases').all()
        return render(request, 'index.html', {
            'page': self,
            'featured_cases': featured_cases,
            'categories': categories,
        })


class AnswersPage(Page):
    intro = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]
    
    parent_page_types = ['wagtailcore.Page']
    subpage_types = []
    
    def serve(self, request):
        from apps.main.models import FAQ
        faqs = FAQ.objects.filter(is_active=True).order_by('order', '-created_at')
        return render(request, 'answers.html', {
            'page': self,
            'faqs': faqs
        })


class AccountPage(Page):
    intro = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]
    
    parent_page_types = ['wagtailcore.Page']
    subpage_types = []
    
    def serve(self, request):
        return render(request, 'account.html', {'page': self})


class DepositPage(Page):
    intro = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]
    
    parent_page_types = ['wagtailcore.Page']
    subpage_types = []
    
    def serve(self, request):
        return render(request, 'deposit.html', {'page': self})


class HistoryPage(Page):
    intro = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]
    
    parent_page_types = ['wagtailcore.Page']
    subpage_types = []
    
    def serve(self, request):
        return render(request, 'history.html', {'page': self})


class OpenCasePage(Page):
    intro = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]
    
    parent_page_types = ['wagtailcore.Page']
    subpage_types = []
    
    def serve(self, request):
        return render(request, 'cases/opencase.html', {'page': self})


class ScrollCasePage(Page):
    intro = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]
    
    parent_page_types = ['wagtailcore.Page']
    subpage_types = []
    
    def serve(self, request):
        return render(request, 'cases/scrollcase.html', {'page': self})


class RequestsPage(Page):
    intro = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]
    
    parent_page_types = ['wagtailcore.Page']
    subpage_types = []
    
    def serve(self, request):
        return render(request, 'requests.html', {'page': self})


class LoginPage(Page):
    intro = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]
    
    parent_page_types = ['wagtailcore.Page']
    subpage_types = []
    
    def serve(self, request):
        if request.user.is_authenticated:
            from django.shortcuts import redirect
            return redirect('index')
        return render(request, 'login.html', {'page': self})
