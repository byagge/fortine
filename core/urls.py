from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views

urlpatterns = [
	path("django-admin/", admin.site.urls),
	path("admin/", include(wagtailadmin_urls)),
	path("documents/", include(wagtaildocs_urls)),
	path("search/", search_views.search, name="search"),
	path("accounts/", include("apps.accounts.urls")),
	path("cases/", include("apps.cases.urls")),
	path("skins/", include("apps.skins.urls")),
	path("api/cases/", include("apps.cases.api_urls")),
	path("api/skins/", include("apps.skins.api_urls")),
	path("finances/", include("apps.finances.urls")),
	# Убираем старые маршруты main, так как теперь они будут обрабатываться Wagtail
	# path("", include("apps.main.urls")),
]


if settings.DEBUG:
	from django.conf.urls.static import static
	from django.contrib.staticfiles.urls import staticfiles_urlpatterns

	# Serve static and media files from development server
	urlpatterns += staticfiles_urlpatterns()
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
	# For anything not caught by a more specific rule above, hand over to
	# Wagtail's page serving mechanism. This should be the last pattern in
	# the list:
	path("", include(wagtail_urls)),
	# Alternatively, if you want Wagtail pages to be served from a subpath
	# of your site, rather than the site root:
	#    path("pages/", include(wagtail_urls)),
]
