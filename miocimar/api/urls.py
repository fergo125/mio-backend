from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

router = DefaultRouter()
router.register(r'tide_regions', views.TideRegionViewSet)
router.register(r'tide_entries', views.TideEntryViewSet)
router.register(r'local_forecasts', views.LocalForecastsViewSet)
router.register(r'local_forecast_entry', views.LocalForecastEntryViewSet, 'local_forecast_entry')

urlpatterns = [
    url(r'^', include(router.urls))
]
