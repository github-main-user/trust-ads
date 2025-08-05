from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from reviews.views import ReviewViewSet

from .apps import AdsConfig
from .views import AdViewSet

app_name = AdsConfig.name


ads_router = DefaultRouter()
ads_router.register("", AdViewSet, "ad")

reviews_router = NestedDefaultRouter(ads_router, "", lookup="ad")
reviews_router.register("reviews", ReviewViewSet, "ads-review")

urlpatterns = [
    *ads_router.urls,
    *reviews_router.urls,
]
