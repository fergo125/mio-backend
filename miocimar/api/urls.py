from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

router = DefaultRouter()
router.register(r'tide_regions', views.TideRegionViewSet)
router.register(r'tide_entries', views.TideEntryViewSet)
router.register(r'local_forecasts', views.LocalForecastsViewSet)
router.register(r'warnings', views.WaveWarningViewSet)
router.register(r'local_forecast_entry', views.LocalForecastEntryViewSet, 'local_forecast_entry')
router.register(r'regional_forecasts', views.RegionalForecastViewSet, 'regional_forecasts')
router.register(r'regional_forecasts_slides', views.RegionalForecastSlides, 'regional_forecasts_slides')


# Drupal connection endpoint
router.register(r'update_local_forecast_data', views.UpdateLocalForecastDataViewSet, 'update_local_forecast_data')
router.register(r'update_regional_forecast_data', views.UpdateRegionalForecastDataViewSet, 'update_regional_forecast_data')
router.register(r'update_warning_data', views.UpdateWarningDataViewSet, 'update_warning_data')

urlpatterns = [
    url(r'^', include(router.urls))
]
