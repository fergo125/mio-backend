from rest_framework import serializers
from api.models import *
from django.views.decorators.csrf import csrf_exempt
#El serializer se encarga de transformar los datos que se leen del modelo y un formato de etiqueta:valor.

class TideRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TideRegion

class TideEntrySerializer(serializers.ModelSerializer):
    #id = serializers.HyperlinkedIdentityField(many=True, view_name='tides-week')
    class Meta:
        model = TideEntry

class LocalForecastSerializer(serializers.ModelSerializer):
    # Get translation texts
    wind_text = serializers.SerializerMethodField("get_localized_wind")
    wave_text = serializers.SerializerMethodField("get_localized_wave")
    temp_text = serializers.SerializerMethodField("get_localized_temp")
    salt_text = serializers.SerializerMethodField("get_localized_salt")
    class Meta:
        model = LocalForecast
        fields = ('id', 'taxonomy_id', 'name', 'english_name', 'small_icon_url', 'medium_icon_url', 'large_icon_url', 'small_map_url', 'medium_map_url', 'large_map_url', 'comment', 'region_map_url', 'wind_text', 'wave_text', 'temp_text', 'salt_text')

    def get_localized_wind(self, obj):
        translation = self.get_translation_object(obj)
        if translation is None:
            return None
        return translation.wind_text

    def get_localized_wave(self, obj):
        translation = self.get_translation_object(obj)
        if translation is None:
            return None
        return translation.wave_text

    def get_localized_temp(self, obj):
        translation = self.get_translation_object(obj)
        if translation is None:
            return None
        return translation.temp_text

    def get_localized_salt(self, obj):
        translation = self.get_translation_object(obj)
        if translation is None:
            return None
        return translation.salt_text

    # Get the translation object for the current forecast,
    # and set language code (comes in the context)
    def get_translation_object(self, obj):
        lang_code = self.context.get("lang")
        res = None
        try:
            lang = Language.objects.get(code=lang_code)
        except:
            lang = Language.objects.get(code="es")

        try:
            return LocalForecastTranslation.objects.get(language=lang, forecast=obj)
        except:
            return None

class LocalForecastEntryCreateSerializer(serializers.ModelSerializer):
    local_forecast = serializers.PrimaryKeyRelatedField(queryset=LocalForecast.objects.all())
    class Meta:
        model = LocalForecastEntry
        fields=('local_forecast', 'date', 'wave_direction', 'wave_height_sig', 'wave_height_max', 'wave_period', 'wind_direction', 'wind_speed', 'wind_burst')

class LocalForecastEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalForecastEntry

class WaveWarningSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaveWarning

class SlideForecastImageSerializer(serializers.ModelSerializer):
    # forecast_id = serializers.PrimaryKeyRelatedField(queryset=RegionalForecast.objects.all())
    class Meta:
        model = SlideForecastImage
        # fields = ('date','url','forecast_id')

class SlideForecastImageNoFKSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlideForecastImage
        fields = ('id','date','url')

class RegionalForecastSerializer(serializers.ModelSerializer):
    slides = SlideForecastImageNoFKSerializer(many=True, read_only=True)
    class Meta:
        model = RegionalForecast
        fields = ('id', 'taxonomy_id', 'name', 'english_name', 'date', 'text', 'animation_url', 'scale_bar_url', 'slides')

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language

class LocalForecastTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalForecastTranslation
