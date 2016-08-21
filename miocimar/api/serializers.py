from rest_framework import serializers
from api.models import *
from django.views.decorators.csrf import csrf_exempt
#El serializer se encarga de transformar los datos que se leen del modelo y un formato de etiqueta:valor.

class TideRegionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TideRegion

class TideEntrySerializer(serializers.HyperlinkedModelSerializer):
    #id = serializers.HyperlinkedIdentityField(many=True, view_name='tides-week')
    class Meta:
        model = TideEntry

class LocalForecastSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LocalForecast

class LocalForecastEntryCreateSerializer(serializers.ModelSerializer):
    local_forecast = serializers.PrimaryKeyRelatedField(queryset=LocalForecast.objects.all())
    class Meta:
        model = LocalForecastEntry
        fields=('local_forecast', 'date', 'wave_direction', 'wave_height_sig', 'wave_height_max', 'wave_period', 'wind_direction', 'wind_speed', 'wind_burst')

class LocalForecastEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalForecastEntry

class WaveWarningSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WaveWarning
