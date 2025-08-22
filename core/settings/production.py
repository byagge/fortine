from .base import *

DEBUG = True

# ManifestStaticFilesStorage is recommended in production, to prevent
# outdated JavaScript / CSS assets being served from cache
# (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/5.2/ref/contrib/staticfiles/#manifeststaticfilesstorage
STORAGES["staticfiles"]["BACKEND"] = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "77.245.157.39", "fortcase.cc", "www.fortcase.cc"]

CSRF_TRUSTED_ORIGINS = ["https://*.77.245.157.39", "https://*.fortcase.cc", "https://*.www.fortcase.cc"]

SECRET_KEY = "q@fwqvk5y8st7#xt*85a9s=&nw0pf3wnhcp32sxqj)z-tuksg$"

try:
    from .local import *
except ImportError:
    pass
