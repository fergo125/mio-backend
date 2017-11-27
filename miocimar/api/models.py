from __future__ import unicode_literals
from django.db import models

"""
Stores the localforecasts info data for each region of the forecasts 
"""

class LocalForecast(models.Model):
	"""LocalForecasts model with metadata relative to 
	the location and other characteristics of the forecast
	for mobile and web. It stores the comments and saves 
	different images resolutions for mobile and web"""

    id = models.AutoField(primary_key=True)
    taxonomy_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=50)
    # If available
    english_name = models.CharField(max_length=50)
    # Region icon
    small_icon_url = models.CharField(max_length=200)
    medium_icon_url = models.CharField(max_length=200)
    large_icon_url = models.CharField(max_length=200)
    # Map
    small_map_url = models.CharField(max_length=200)
    medium_map_url = models.CharField(max_length=200)
    large_map_url = models.CharField(max_length=200)
    # This comment should be updated each time a new Drupal
    # article appears
    comment = models.CharField(max_length=4000)
    region_map_url = models.CharField(max_length=200, default="")
    def __unicode__(self):
        return self.name

class LocalForecastEntry(models.Model):
	"""
	Stores the variables' entries the for a specific local forecast region.
	"""
    id = models.AutoField(primary_key=True)
    local_forecast = models.ForeignKey(LocalForecast, on_delete =models.CASCADE)
    date = models.DateTimeField()
    wave_direction = models.FloatField()
    wave_height_sig = models.FloatField()
    wave_height_max = models.FloatField()
    wave_period = models.FloatField()
    wind_direction = models.FloatField()
    wind_speed = models.FloatField()
    wind_burst = models.FloatField()

class TideRegion(models.Model):
	"""
	Model for tides regions with metadata of each tide region 
	of the forecast.It stores different image resolutions for mobile and web"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    # If available
    english_name = models.CharField(max_length=50)
    # Region icon
    small_icon_url = models.CharField(max_length=200)
    medium_icon_url = models.CharField(max_length=200)
    large_icon_url = models.CharField(max_length=200)
    medium_level = models.FloatField()
    order = models.IntegerField()
    mean_highest_tides = models.FloatField(default=0)

    def __unicode__(self):
        return self.name


class TideEntry(models.Model):
	"""
	Stores the variables' entries the for a specific local forecast region.
	"""
    id = models.AutoField(primary_key=True)
    tide_region = models.ForeignKey(TideRegion, on_delete=models.CASCADE)
    date = models.DateTimeField()
    tide_height = models.FloatField()
    is_high_tide = models.BooleanField()
    moon = models.IntegerField()

class RegionalForecast(models.Model):
    id = models.AutoField(primary_key=True)
    taxonomy_id = models.IntegerField(unique=True)

    name = models.CharField(max_length=50)
    # If available
    english_name = models.CharField(max_length=50)

    # These values are updated for each new Drupal node
    date = models.DateTimeField()
    text = models.TextField()
    animation_url = models.CharField(max_length=200)
    scale_bar_url = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class SlideForecastImage(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField()
    url = models.CharField(max_length=400)
    forecast_id = models.ForeignKey(RegionalForecast, related_name='slides', on_delete=models.CASCADE)

class WaveWarning(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    level = models.IntegerField()
    date = models.DateTimeField()
    text = models.TextField()

    def __unicode__(self):
        return self.title

class Language(models.Model):
    # Language object (used for localization/internationalization)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=2)

    def __unicode__(self):
        return self.name


class LocalForecastTranslation(models.Model):
    # Object which contains translations for LocalForecast (regions)
    id = models.AutoField(primary_key=True)
    language = models.ForeignKey(Language, related_name="language")
    forecast = models.ForeignKey(LocalForecast, related_name="forecast")
    wind_text = models.TextField()
    wave_text = models.TextField()
    temp_text = models.TextField()
    salt_text = models.TextField()
