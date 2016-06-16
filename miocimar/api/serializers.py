from rest_framework import serializers
from api.models import *
from django.views.decorators.csrf import csrf_exempt
#El serializer se encarga de transformar los datos que se leen del modelo y un formato de etiqueta:valor.

class TideRegionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TideRegion
        fields = ('url','id','name','icon_url')

class TideEntrySerializer(serializers.HyperlinkedModelSerializer):
    #id = serializers.HyperlinkedIdentityField(many=True, view_name='tides-week')
    class Meta:
        model = TideEntry
        fields = ('id','tide_region','date','tide_height','is_high_tide')

class LocalForecastSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LocalForecast
        fields=('url','id','name','icon_url')
