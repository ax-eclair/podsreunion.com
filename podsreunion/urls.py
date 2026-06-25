from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.views import serve as serve_static
from django.urls import path, re_path

from pages import views

urlpatterns = [
    path("", views.home, name="home"),
    path("impressum.html", views.impressum, name="impressum"),
    path("datenschutz.html", views.datenschutz, name="datenschutz"),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r"^static/(?P<path>.*)$", serve_static, kwargs={"insecure": True}),
    ]
