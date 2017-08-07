from __future__ import unicode_literals
from django.db import models

class LocalForecast(models.Model):
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
    mean_highest_tides = models.FloatField()

    def __unicode__(self):
        return self.name


class TideEntry(models.Model):
    id = models.AutoField(primary_key=True)
    tide_region = models.ForeignKey(TideRegion, on_delete=models.CASCADE)
    date = models.DateTimeField()
    tide_height = models.FloatField(    )
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
    timestamp = models.DateTimeField()
    url = models.CharField(max_length=400)
    forecast_id = models.ForeignKey(RegionalForecast, on_delete=models.CASCADE)

class WaveWarning(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    level = models.IntegerField()
    date = models.DateTimeField()
    text = models.TextField()

    def __unicode__(self):
        return self.title
