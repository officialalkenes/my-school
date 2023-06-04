from django.conf import settings

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.school.urls", namespace="school")),
    path("accounts/", include("apps.user.urls", namespace="accounts")),
]
