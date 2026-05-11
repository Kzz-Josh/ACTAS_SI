from .base import *  # noqa

DEBUG = True
ALLOWED_HOSTS = ["*"]
INSTALLED_APPS += ["django_extensions"]  # type: ignore # noqa

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
