from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.views import serve as serve_static
from django.urls import path, re_path

from pages import views

urlpatterns = [
    path("", views.home, name="home"),
    path("sell/", views.SellerSubmissionView.as_view(), name="seller_submission"),
    path("impressum.html", views.impressum, name="impressum"),
    path("datenschutz.html", views.datenschutz, name="datenschutz"),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r"^static/(?P<path>.*)$", serve_static, kwargs={"insecure": True}),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
