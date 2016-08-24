import logging

from django.shortcuts import render
from api.models import *
from api.serializers import *
from django.http import Http404
from rest_framework.decorators import detail_route
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from django.views.decorators.csrf import csrf_exempt
import datetime
import automation.data_update as data_updater
import json

logger = logging.getLogger("mioLogger")

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

class WaveWarningViewSet(ModelViewSet):
    """ Warning entries view set, mainly for creating new items."""
    queryset = WaveWarning.objects.all()
    serializer_class = WaveWarningSerializer

class LocalForecastsViewSet(ModelViewSet):
    """ Local forecasts view set """
    queryset = LocalForecast.objects.all()
    serializer_class = LocalForecastSerializer

    @detail_route(methods=['get'])
    def weekly_view(self, request, **kwargs):
        """Obtain a list of local forecast entries for this local forecast
        region for this week
        """
        local_forecast_region = self.get_object()
        pk = local_forecast_region.pk
        start_date = datetime.date.today() - datetime.timedelta(days=1)
        end_date = datetime.date.today() + datetime.timedelta(days=7)
        local_forecast_entries = LocalForecastEntry.objects \
            .filter(date__gt=start_date) \
            .filter(date__lt=end_date) \
            .filter(local_forecast=pk)
        serializer = LocalForecastEntrySerializer(local_forecast_entries, context={'request': request}, many=True)
        return Response(serializer.data)


class LocalForecastEntryViewSet(ModelViewSet):
    queryset = LocalForecastEntry.objects.all()
    serializer_class = LocalForecastEntrySerializer

    '''def list(self, request):
        entries = LocalForecastEntry.objects.all()
        serializer = LocalForecastEntrySerializer(entries, many=True)
        return Response(serializer.data)'''

    def create(self, request):
        serialized_list = LocalForecastEntryCreateSerializer(data=request.data, many=True)
        # Check if list could be serialized correctly
        if serialized_list.is_valid():

            # Run one by one each new object
            for serialized_object in serialized_list.data:

                # Check if this entry already exists (using region and date)
                forecast_region  = serialized_object['local_forecast']
                forecast_date    = serialized_object['date']
                existing_entries = LocalForecastEntry.objects  \
                    .filter(local_forecast=forecast_region)  \
                    .filter(date=forecast_date)

                if existing_entries is not None and len(existing_entries) > 0:

                    # There was an entry for it already
                    existing_entry = existing_entries[0]
                    update_entry = LocalForecastEntryCreateSerializer(existing_entry, data=serialized_object)
                    if update_entry.is_valid():
                        update_entry.save()
                    else:
                        # TODO: Update this to a logging statement later
                        print "Couldn't serialize and update this entry: " + str(serialized_object)
                else:

                    # There was no previous object
                    new_entry = LocalForecastEntryCreateSerializer(data=serialized_object)
                    if new_entry.is_valid():
                        new_entry.save()
                    else:
                        # TODO: Update this to a logging statement later
                        print "Couldn't serialize and create this entry: " + str(serialized_object)

            return Response({"result": "success", "message": "Successfully saved"})
        else:
            return Response({"result": "error", "message": "Invalid serializer data"})

# Drupal connection endpoints
class UpdateLocalForecastDataViewSet(ViewSet):
    def create(self, request):
        if "node_id" not in request.data:
            logger.error("node_id not found in request")

        node_id = request.data["node_id"]
        logger.debug("Local Forecast update, node id: {0}".format(node_id))
        content = {'working': 'OK', "node_id": node_id}
        return Response(content, status=status.HTTP_200_OK)

class UpdateRegionalForecastDataViewSet(ViewSet):
    def create(self, request):
        if "node_id" not in request.data:
            logger.error("node_id not found in request")

        node_id = request.data["node_id"]
        logger.debug("Regional Forecast update, node id: {0}".format(node_id))
        content = {'working': 'OK', "node_id": node_id}
        return Response(content, status=status.HTTP_200_OK)

class UpdateWarningDataViewSet(ViewSet):
    def create(self, request):
        if "node_id" not in request.data:
            logger.error("node_id not found in request")

        node_id = request.data["node_id"]
        logger.debug("Warning update, node id: {0}".format(node_id))
        content = {'working': 'OK', "node_id": node_id}
        return Response(content, status=status.HTTP_200_OK)
