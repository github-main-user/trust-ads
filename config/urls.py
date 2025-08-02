from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # admin
    path("admin/", admin.site.urls),
    # apps
    path("api/v1/users/", include("users.urls")),
]
