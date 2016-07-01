from django.shortcuts import render
from api.models import *
from api.serializers import *
from django.http import Http404
from rest_framework.decorators import detail_route
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
import datetime

class TideRegionViewSet(ModelViewSet):
    """Tide regions view set, which also includes a weekly view for
    its tide entries.
    """
    queryset = TideRegion.objects.all()
    serializer_class = TideRegionSerializer

    @csrf_exempt
    @detail_route(methods=['get'])
    def weekly_view(self, request, **kwargs):
        """Obtain a list of tide entries for this tide region for this
        week
        """
        tide_region = self.get_object()
        pk = tide_region.pk
        start_date = datetime.date.today() - datetime.timedelta(days=1)
        end_date = datetime.date.today() + datetime.timedelta(days=7)
        tides = TideEntry.objects \
            .filter(date__gt=start_date) \
            .filter(date__lt=end_date) \
            .filter(tide_region=pk)
        serializer = TideEntrySerializer(tides, context={'request': request}, many=True)
        return Response(serializer.data)

class TideEntryViewSet(ModelViewSet):
    """ Tide entries view set, mainly for creating new items."""
    queryset = TideEntry.objects.all()
    serializer_class = TideEntrySerializer

class LocalForecastsViewSet(ModelViewSet):
    """ Local forecasts view set """
    queryset = LocalForecast.objects.all()
    serializer_class = LocalForecastSerializer

class LocalForecastEntryViewSet(ModelViewSet):
    queryset = LocalForecastEntry.objects.all()
    serializer_class = LocalForecastSerializer
    @csrf_exempt
    @detail_route(methods=['put'])
    def put(self,request,**kwargs):
        newEntries = LocalForecastEntrySerializer(request.data)
        print(newEntries)
        existingEntries = LocalForecastEntry.objects.all()
        for newEntry in newEntries:
            modifyEntry = existingEntries.filter(local_forecast=newEntry['local_forecast']).filter(date=newEntry['date'])
            if newEntry is not None :
                # modifyEntry.wave_direction = newEntry['wave_direction']
                # modifyEntry.wave_height_sig = newEntry['wave_height_sig']
                # modifyEntry.wave_height_max = newEntry['wave_height_max']
                # modifyEntry.wave_period  = newEntry['wave_period']
                # modifyEntry.wind_direction = newEntry['wind_direction']
                # modifyEntry.wind_speed = newEntry['wind_speed']
                # modifyEntry.wind_burst = newEntry['wind_burst']
                # modifyEntry.save()
                modifyEntry.update(wave_direction = newEntry['wave_direction'],wave_height_sig = newEntry['wave_height_sig'], \
                wave_period  = newEntry['wave_period'],wave_height_max = newEntry['wave_height_max'], \
                wind_direction = newEntry['wind_direction'],wind_speed = newEntry['wind_speed'], \
                wind_burst = newEntry['wind_burst'])
            else:
                newEntry.save()
                # entry = LocalForecastEntry(local_forecast = newEntry['local_forecast'],date = newEntry['date'],\
                # wave_direction = newEntry['wave_direction'],wave_height_sig = newEntry['wave_height_sig'], \
                # wave_period  = newEntry['wave_period'],wave_height_max = newEntry['wave_height_max'], \
                # wind_direction = newEntry['wind_direction'],wind_speed = newEntry['wind_speed'], \
                # wind_burst = newEntry['wind_burst'])
                entry.save()
