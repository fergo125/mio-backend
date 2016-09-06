from __future__ import unicode_literals
from django.db import models

class LocalForecast(models.Model):
    id = models.AutoField(primary_key=True)
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
    comment = models.CharField(max_length=2000)
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
    """
    @classmethod
    def create(cls,values):
        localForecastEntry = cls(local_forecast=values['local_forecast'],\
        date = values['date'],\
        wave_direction = values['wave_direction'],\
        wave_height_sig = values['wave_height_sig'],\
        wave_height_max = values['wave_height_max'],\
        wave_period = values['wave_period'],\
        wind_direction = values['wind_direction'],\
        wind_speed = values['wind_speed'],\
        wind_burst = values['wind_burst'])
    """
class TideRegion(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    # If available
    english_name = models.CharField(max_length=50)
    # Region icon
    small_icon_url = models.CharField(max_length=200)
    medium_icon_url = models.CharField(max_length=200)
    large_icon_url = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class TideEntry(models.Model):
    id = models.AutoField(primary_key=True)
    tide_region = models.ForeignKey(TideRegion, on_delete =models.CASCADE)
    date = models.DateTimeField()
    tide_height = models.FloatField()
    is_high_tide = models.BooleanField()

class RegionalForecast(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    # If available
    english_name = models.CharField(max_length=50)
    # Type icon
    small_icon_url = models.CharField(max_length=200)
    medium_icon_url = models.CharField(max_length=200)
    large_icon_url = models.CharField(max_length=200)

    # These values are updated for each new Drupal node
    date = models.DateField()
    text = models.TextField()
    animation_url = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class WaveWarning(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    level = models.IntegerField()
    date = models.DateTimeField()
    text = models.TextField()

    def __unicode__(self):
        return self.title
