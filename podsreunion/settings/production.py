import os

import dj_database_url

from . import *  # noqa: F403

DEBUG = False
SECRET_KEY = os.environ["SECRET_KEY"]
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", ".herokuapp.com,podsreunion.com").split(",")
CSRF_TRUSTED_ORIGINS = [
    origin
    for origin in os.environ.get(
        "CSRF_TRUSTED_ORIGINS",
        "https://*.herokuapp.com,https://podsreunion.com",
    ).split(",")
    if origin
]

DATABASES = {
    "default": dj_database_url.config(
        env="DATABASE_URL",
        conn_max_age=600,
        ssl_require=True,
    )
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    *MIDDLEWARE[1:],  # noqa: F405
]
STORAGES["staticfiles"]["BACKEND"] = (  # noqa: F405
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
)

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", "true").lower() == "true"
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
