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
from django.utils import timezone
from dateutil.tz import tzlocal
import datetime
import automation.data_update as data_updater
import json
import time
import dateutil.parser
import itertools
import thread
import pytz

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
        start_date = datetime.date.today() - datetime.timedelta(days=1)
        end_date = datetime.date.today() + datetime.timedelta(days=7)

        tides = TideEntry.objects \
            .filter(date__gt=start_date) \
            .filter(date__lt=end_date) \
            .filter(tide_region=tide_region.pk)

        serializer = TideEntrySerializer(tides, context={'request': request}, many=True)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def search_date(self, request, **kwargs):
        tide_region = self.get_object()
        start_date = dateutil.parser.parse(request.query_params.get('start'))
        end_date = dateutil.parser.parse(request.query_params.get('end'))

        # Strip time from datetimes
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = end_date.replace(hour=0, minute=0, second=0, microsecond=0)

        # Make end_date inclusive
        end_date = end_date + datetime.timedelta(days=1)
        tides = TideEntry.objects \
            .filter(date__gt=start_date) \
            .filter(date__lt=end_date) \
            .filter(tide_region=tide_region.pk)

        serializer = TideEntrySerializer(tides, context={'request': request}, many=True)
        return Response(serializer.data)

class TideEntryViewSet(ModelViewSet):
    """ Tide entries view set, mainly for creating new items."""
    queryset = TideEntry.objects.all()
    serializer_class = TideEntrySerializer

class WaveWarningViewSet(ModelViewSet):
    """ Warning entries view set, mainly for creating new items."""
    queryset = WaveWarning.objects.order_by('-date')
    serializer_class = WaveWarningSerializer

    def list(self, request):
        # Get the last 10 informative notifications (level = 0)
        notifications = list(WaveWarning.objects.order_by('-date').filter(level = 0)[:10])
        # Get the last 10 alert notifications (level > 0)
        alerts = list(WaveWarning.objects.order_by('-date').filter(level__gt = 0)[:10])
        joined_list = notifications + alerts
        serializer = WaveWarningSerializer(joined_list, context={'request': request}, many=True)
        return Response(serializer.data)

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

        # Find latest record
        latest = LocalForecastEntry.objects.filter(local_forecast=pk) \
            .order_by('-date')[:1][0]
        start_date = latest.date - datetime.timedelta(days=7)

        local_forecast_entries = LocalForecastEntry.objects \
            .filter(date__gt=start_date) \
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
        status_return = status.HTTP_200_OK
        time.sleep(5)
        if "node_id" not in request.data:
            logger.error("node_id not found in request")
            status_return = status.HTTP_404_NOT_FOUND
            content = {'Message':'node_id not found in request'}
        else:
            node_id = request.data["node_id"]
            logger.debug("Local Forecast update, node id: {0}".format(node_id))
            thread.start_new_thread(data_updater.localForecastUpdate,(node_id,))
            content = {'Updated':node_id,'Element-type':"Local Forecast entry"}
        return Response(content, status=status_return)

class UpdateRegionalForecastDataViewSet(ViewSet):
    def create(self, request):
        status_return = status.HTTP_200_OK
        if "node_id" not in request.data:
            logger.error("node_id not found in request")
            status_return = status.HTTP_404_NOT_FOUND
            content = {'Message':'node_id not found in request'}
        else:
            node_id = request.data["node_id"]
            logger.debug("Regional Forecast update, node id: {0}".format(node_id))
            thread.start_new_thread(data_updater.regionalForecastUpdate,(node_id,))
            content = {'Updated':node_id,'Element-type':"Regional Forecast"}
        return Response(content, status=status_return)

class UpdateWarningDataViewSet(ViewSet):
    def create(self, request):
        status_return = status.HTTP_200_OK
        if "node_id" not in request.data:
            logger.error("node_id not found in request")
            status_return = status.HTTP_404_NOT_FOUND
            content = {'Message':'node_id not found in request'}
        else:
            node_id = request.data["node_id"]
            logger.debug("Local Forecast update, node id: {0}".format(node_id))
            thread.start_new_thread(data_updater.warningUpdate,(node_id,))
            content = {'Updated':node_id,'Element-type':"Warning entry"}
        return Response(content, status=status_return)

class RegionalForecastViewSet(ModelViewSet):
    queryset = RegionalForecast.objects.all()
    serializer_class = RegionalForecastSerializer

class DrupalTidesViewset(ViewSet):
    def list(self,request,format):
        print(request.query_params)
        print(request.data)
        if "tide_region" not in request.query_params:
            logger.error("tide_region not found in request")
            status_return = status.HTTP_404_NOT_FOUND
            content = {'Message':'tide_region not found in request'}
            return Response(content,status=status_return)
        else:
            costa_rica_tz = pytz.timezone('America/Costa_Rica')
            begin_date = datetime.datetime.now(costa_rica_tz)
            end_date = timezone.now()+ datetime.timedelta(days=7)

            if "begin_date" in request.query_params and "end_date" in request.query_params:
                begin_date = request.query_params['begin_date']
                end_date = request.query_params['end_date']
            begin_date = begin_date.replace(hour=0,minute=0,microsecond=0)
            end_date = end_date.replace(hour=0,minute=0,microsecond=0)
            actual_tides = TideEntry.objects.filter(date__gt=begin_date,\
                date__lt=end_date,\
                tide_region=request.query_params['tide_region'])
            previous_day = begin_date - datetime.timedelta(days=1)
            previous_day_items = TideEntry.objects.filter(date__gt=previous_day,date__lt=begin_date)
            previous_day_last_item = previous_day_items[len(previous_day_items)-1]
            epoch = datetime.datetime.now(costa_rica_tz)
            epoch = epoch.replace(year=1970,month=1,day=1,hour=0,minute=0,second=0,microsecond=0)
            response_list = list()
            last_item_date = int((previous_day_last_item.date.replace(tzinfo=epoch.tzinfo) - epoch).total_seconds()*1000)
            response_list.append([last_item_date,previous_day_last_item.tide_height])
            for tide in actual_tides:
                response_elements = list()
                #tide_date = int((tide.date.replace(tzinfo=None) - epoch).total_seconds()*1000)
                tide_date = int((tide.date.replace(tzinfo=epoch.tzinfo) - epoch).total_seconds()*1000)
                response_list.append([tide_date,tide.tide_height])
            medium_level = (TideRegion.objects.filter(id = request.query_params['tide_region'])[0]).medium_level
            response_dict = dict()
            response_dict['medium_level'] = medium_level
            response_dict['days'] = response_list
            status_return = status.HTTP_200_OK
            print(response_dict)
            return Response(response_dict,status= status_return)
        # for key in request.data:
        #     print('key: '+ key)
        # if "tide_region" not in request.data:
        #     logger.error("tide_region not found in request")
        #     status_return = status.HTTP_404_NOT_FOUND
        #     content = {'Message':'tide_region not found in request'}
        #     return Response(content,status=status_return)
        # else:
        #     actual_tides = TideEntry.objects.filter(date__gt=datetime.datetime.now(),\
        #         date__lt=(datetime.datetime.now()+ datetime.timedelta(days=3)),\
        #         tide_region=request.data['tide_region'])
        #     epoch = datetime.datetime.utcfromtimestamp(0)
        #     response_tides = dict()
        #     for tide in actual_tides:
        #         tide_date = int((tide.date- epoch).total_seconds() * 1000)
        #         response_tides[tide_date]=tide.tide_height
        #     return Response(json.dumps(response_tides))
