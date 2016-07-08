from __future__ import unicode_literals
from django.db import models

class LocalForecast(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    icon_url = models.CharField(max_length=200)

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
    icon_url = models.CharField(max_length=200)

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
    icon_url = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class RegionalForecastEntry(models.Model):
    id = models.AutoField(primary_key=True)
    regional_forecast = models.ForeignKey(RegionalForecast, on_delete =models.CASCADE)
    date = models.DateField()
    title = models.CharField(max_length=100)
    text = models.TextField()
    animation_url = models.CharField(max_length=200)

class Warning(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    level = models.IntegerField()
    date = models.DateField()
    text = models.TextField()

    def __unicode__(self):
        return self.title
