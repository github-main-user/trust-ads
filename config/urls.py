from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # admin
    path("admin/", admin.site.urls),
    # docs
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/docs/", SpectacularSwaggerView.as_view(), name="swagger-ui"),
    path("api/v1/redoc/", SpectacularRedocView.as_view(), name="redoc"),
    # apps
    path("api/v1/users/", include("users.urls")),
    path("api/v1/ads/", include("ads.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, decument_root=settings.MEDIA_ROOT)
