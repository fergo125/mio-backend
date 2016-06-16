from django.shortcuts import render
from api.models import *
from api.serializers import *
from django.http import Http404
from rest_framework.decorators import detail_route
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework import status
import datetime

class TideRegionViewSet(ModelViewSet):
    """Tide regions view set, which also includes a weekly view for
    its tide entries.
    """
    queryset = TideRegion.objects.all()
    serializer_class = TideRegionSerializer

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
