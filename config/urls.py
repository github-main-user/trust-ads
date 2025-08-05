from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # admin
    path("admin/", admin.site.urls),
    # apps
    path("api/v1/users/", include("users.urls")),
    path("api/v1/ads/", include("ads.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, decument_root=settings.MEDIA_ROOT)
