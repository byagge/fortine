from django.db import models

from wagtail.models import Page
from django.shortcuts import render


class HomePage(Page):
	pass

class StaticTemplatePage(Page):
	template_name_override = models.CharField(max_length=255, blank=True, help_text="Django template path to render")
	
	content_panels = Page.content_panels + [
		# We keep it minimal; editors set slug/title and template path
	]
	
	subpage_types = []
	parent_page_types = ['wagtailcore.Page']
	
	def serve(self, request):
		tpl = (self.template_name_override or '').strip() or None
		if not tpl:
			return super().serve(request)
		return render(request, tpl, {})

# Dedicated page models for existing site templates
class IndexPage(Page):
	parent_page_types = ['wagtailcore.Page']
	subpage_types = []
	def serve(self, request):
		return render(request, 'index.html', {})

class AnswersPage(Page):
	parent_page_types = ['wagtailcore.Page']
	subpage_types = []
	def serve(self, request):
		return render(request, 'answers.html', {})

class AccountPage(Page):
	parent_page_types = ['wagtailcore.Page']
	subpage_types = []
	def serve(self, request):
		return render(request, 'account.html', {})

class DepositPage(Page):
	parent_page_types = ['wagtailcore.Page']
	subpage_types = []
	def serve(self, request):
		return render(request, 'deposit.html', {})

class HistoryPage(Page):
	parent_page_types = ['wagtailcore.Page']
	subpage_types = []
	def serve(self, request):
		return render(request, 'history.html', {})

class OpenCasePage(Page):
	parent_page_types = ['wagtailcore.Page']
	subpage_types = []
	def serve(self, request):
		return render(request, 'cases/opencase.html', {})

class ScrollCasePage(Page):
	parent_page_types = ['wagtailcore.Page']
	subpage_types = []
	def serve(self, request):
		return render(request, 'cases/scrollcase.html', {})

class RequestsPage(Page):
	parent_page_types = ['wagtailcore.Page']
	subpage_types = []
	def serve(self, request):
		return render(request, 'requests.html', {})
