from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("staff_management.urls", namespace="staff_management")),
    path("accounts/", include("django.contrib.auth.urls")),
]
