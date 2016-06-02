from __future__ import unicode_literals

from django.db import models
class LocalForecast(models.Model):
    id= models.AutoField(primary_key=True)
    name= models.CharField(max_length=50)
    icon_url= models.CharField(max_length=100)

class LocalForecastEntry(models.Model):
    id = models.AutoField(primary_key=True)
    local_forecast = models.ForeignKey(LocalForecast, on_delete =models.CASCADE)
    date = models.DateField()
    wave_direction = models.FloatField()
    wave_height_sig = models.FloatField()
    wave_height_max = models.FloatField()
    wave_period = models.FloatField()
    wind_direction = models.FloatField()
    wind_speed = models.FloatField()
    wind_burst = models.FloatField()

class TideRegion(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    icon_url = models.CharField(max_length=100)

class TideEntry(models.Model):
    id = models.AutoField(primary_key=True)
    tide_region = models.ForeignKey(TideRegion, on_delete =models.CASCADE)
    date = models.DateField()
    tide_height = models.FloatField()
    is_high_tide = models.BooleanField()


# Create your models here.
