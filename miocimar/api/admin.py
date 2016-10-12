from django.contrib import admin

# Register your models here.
from api.models import LocalForecast, TideRegion, RegionalForecast, WaveWarning

admin.site.register(LocalForecast)
admin.site.register(TideRegion)
admin.site.register(RegionalForecast)
admin.site.register(WaveWarning)