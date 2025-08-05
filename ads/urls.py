from rest_framework.routers import DefaultRouter

from .apps import AdsConfig
from .views import AdViewSet

app_name = AdsConfig.name


ads_router = DefaultRouter()
ads_router.register("", AdViewSet, "ad")

urlpatterns = [
    *ads_router.urls,
]
