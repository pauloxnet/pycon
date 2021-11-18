from .base import *  # noqa

SECRET_KEY = "do not use this in production"
SLACK_INCOMING_WEBHOOK_URL = ""
USE_SCHEDULER = False

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

PASTAPORTO_SECRET = env("PASTAPORTO_SECRET", default="pastaporto_xxxxxxxx")

USERS_SERVICE = env("USERS_SERVICE")
SERVICE_TO_SERVICE_SECRET = env("SERVICE_TO_SERVICE_SECRET")
