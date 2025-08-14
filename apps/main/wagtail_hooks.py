from wagtail import hooks
from wagtail.admin.menu import MenuItem

class RequestsMenuItem(MenuItem):
	def is_shown(self, request):
		return bool(request.user and request.user.is_staff)

@hooks.register('register_admin_menu_item')
def register_requests_menu_item():
	return RequestsMenuItem(
		'Latest wins',
		'/requests/',
		icon_name='list-ul',
		order=10000,
	)

@hooks.register('register_admin_menu_item')
def register_django_admin_link():
	return MenuItem('Django admin', '/django-admin/', icon_name='site', order=10001) 