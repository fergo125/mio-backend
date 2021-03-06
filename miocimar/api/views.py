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

	get:
	Obtain a list of tide entries for this tide region for this
		week
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
	"""Collection of endpoint for Local"""
	queryset = LocalForecast.objects.all()
	serializer_class = LocalForecastSerializer

	def get_serializer_context(self):
		return {
			'request': self.request,
			# Pass the language header in the serializer context
			'lang': self.request.META.get('HTTP_ACCEPT_LANGUAGE')
		}

	@detail_route(methods=['get'])
	def weekly_view(self, request, **kwargs):
		local_forecast_region = self.get_object()
		pk = local_forecast_region.pk
		# Find latest record
		latest = LocalForecastEntry.objects.filter(local_forecast=pk) \
			.order_by('-date')[:1][0]
		print("Exact hour", datetime.datetime.today())
		start_date = datetime.datetime.today()
		
		start_date -= datetime.timedelta(hours=6)
		print("Hour with adjustment", start_date)
		start_date = start_date.replace(hour=0).replace(minute=0).replace(second=0)
		end_date = start_date + datetime.timedelta(days=7) 
		#end_date = start_date.replace(hour=0).replace(minute=0).replace(second=0)
		print("start date", start_date)
		print("end date", end_date)
		local_forecast_entries = LocalForecastEntry.objects \
			.filter(date__gt=start_date) \
			.filter(date__lte=end_date)\
			.filter(local_forecast=pk)
		print("cantidad de datos", len(local_forecast_entries))
		serializer = LocalForecastEntrySerializer(local_forecast_entries, context={'request': request}, many=True)
		return Response(serializer.data)
	
	@detail_route(methods=['post'])
	def add_new_forecast_data(self, request, **kwargs):
		result = data_updater.proces_csv_parameters(request.data["csv_file"],localforecast_id=request.data["id"])
		status_return = status.HTTP_200_OK
		if result:
			logger.debug('Local Forecast data updated')
			content = {'Local  data added'}
		else:
			status_return = status.HTTP_404_NOT_FOUND
			content = {'Message':'Error adding local Forecast'}
		return Response(content, status=status_return)

class LocalForecastEntryViewSet(ModelViewSet):
	"""Forecast endpoint for creating new forecast entries based
	on new csv files added on the drupal webpage.
	Ask if this endpoint is really used"""

	queryset = LocalForecastEntry.objects.all()
	serializer_class = LocalForecastEntrySerializer

	def create(self, request):
		result = data_updater.proces_csv_parameters(request.data["csv_file"],localforecast_id=request.data["id"])
		status_return = status.HTTP_200_OK
		if result:
			logger.debug('Local Forecast data updated')
			content = {'Local  data added'}
		else:
			status_return = status.HTTP_404_NOT_FOUND
			content = {'Message':'Error adding local Forecast'}
		return Response(content, status=status_return)
		# serialized_list = LocalForecastEntryCreateSerializer(data=request.data, many=True)
		# # Check if list could be serialized correctly
		# if serialized_list.is_valid():

		# 	# Run one by one each new object
		# 	for serialized_object in serialized_list.data:
		# 		# Check if this entry already exists (using region and date)
		# 		forecast_region  = serialized_object['local_forecast']
		# 		forecast_date    = serialized_object['date']
		# 		existing_entries = LocalForecastEntry.objects  \
		# 			.filter(local_forecast=forecast_region)  \
		# 			.filter(date=forecast_date)

		# 		if existing_entries is not None and len(existing_entries) > 0:

		# 			# There was an entry for it already
		# 			existing_entry = existing_entries[0]
		# 			update_entry = LocalForecastEntryCreateSerializer(existing_entry, data=serialized_object)
		# 			if update_entry.is_valid():
		# 				update_entry.save()
		# 			else:
		# 				# TODO: Update this to a logging statement later
		# 				print "Couldn't serialize and update this entry: " + str(serialized_object)
		# 		else:
		# 			# There was no previous object
		# 			new_entry = LocalForecastEntryCreateSerializer(data=serialized_object)
		# 			if new_entry.is_valid():
		# 				new_entry.save()
		# 			else:
		# 				# TODO: Update this to a logging statement later
		# 				print "Couldn't serialize and create this entry: " + str(serialized_object)

		# 	return Response({"result": "success", "message": "Successfully saved"})
		# else:
		# 	return Response({"result": "error", "message": "Invalid serializer data"})

# Drupal connection endpoints
class UpdateLocalForecastDataViewSet(ViewSet):
	"""Local Forecast update endpoint. When the forecast is updated in the Drupal webpage, 
	it sends a csv to the API in order to update the forecast entries"""
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
	"""Regional Forecast update endpoint. When the forecast is updated in the Drupal webpage, 
	it sends a JSON with its content and the """
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
	"""Warning update endpoint. When a new warning is added in the Drupal webpage, 
	it sends its content to the endpoint in order to be added in the API"""
	def create(self, request):
		status_return = status.HTTP_200_OK
		if "node_id" not in request.data:
			logger.error("node_id not found in request")
			status_return = status.HTTP_404_NOT_FOUND
			content = {'Message':'node_id not found in request'}
		else:
			node_id = request.data["node_id"]
			logger.debug("Local Forecast update, node id: {0}".format(node_id))
			thread.start_new_thread(data_updater.warningUpdate, (node_id,))
			content = {'Updated':node_id, 'Element-type':"Warning entry"}
		return Response(content, status=status_return)

class RegionalForecastViewSet(ModelViewSet):
	"""Enpoint for Reginal Forecasts"""
	queryset = RegionalForecast.objects.all()
	serializer_class = RegionalForecastSerializer

class DrupalTidesViewset(ViewSet):
	"""
	Enpoint for tides requests handling.
	list: Returns a list of tides records from a specific TideRegionZone
	starting from today's date or from a given date.
	"""
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
			if "begin_date" in request.query_params:
				begin_date = datetime.datetime.strptime(request.query_params['begin_date'],"%d-%m-%Y")
			end_date = begin_date + datetime.timedelta(days=7)
			begin_date = begin_date.replace(hour=0,minute=0,microsecond=0)
			end_date = end_date.replace(hour=0,minute=0,microsecond=0)
			actual_tides = TideEntry.objects.filter(date__gt=begin_date,\
				date__lt=end_date,\
				tide_region=request.query_params['tide_region'])
			previous_day = begin_date - datetime.timedelta(days=1)
			previous_day_items = TideEntry.objects.filter(date__gt=previous_day,date__lt=begin_date,tide_region=request.query_params['tide_region'])
			previous_day_last_item = previous_day_items[len(previous_day_items)-1]
			epoch = datetime.datetime.now(costa_rica_tz)
			epoch = epoch.replace(year=1970,month=1,day=1,hour=0,minute=0,second=0,microsecond=0)
			response_list = list()
			last_item_date = int((previous_day_last_item.date.replace(tzinfo=epoch.tzinfo) - epoch).total_seconds()*1000)
			response_list.append([last_item_date,previous_day_last_item.tide_height])
			for tide in actual_tides:
				response_elements = list()

				tide_date = int((tide.date.replace(tzinfo=epoch.tzinfo) - epoch).total_seconds()*1000)
				response_list.append([tide_date,tide.tide_height])
			tr = (TideRegion.objects.filter(id = request.query_params['tide_region'])[0])
			response_dict = dict()
			response_dict['medium_level'] = tr.medium_level
			response_dict['mean_highest_tides'] =tr.mean_highest_tides
			response_dict['days'] = response_list
			status_return = status.HTTP_200_OK
			print(response_dict)
			return Response(response_dict, status= status_return)

class RegionalForecastSlides(ViewSet):
	"""
		Enpoint for animation slides handling.abs
		list: Returns a list of slides recently updated and stored in an external domain.
		create: 
	"""
	def list(self,request):
		status_return = status.HTTP_200_OK
		print(request.query_params)
		if "forecast_id" not in request.query_params:
			logger.error("forecast_id not found in request")
			status_return = status.HTTP_404_NOT_FOUND
			content = {'Message':'forecast_id not found in request'}
		else:
			slides = SlideForecastImage.objects.filter(forecast_id=request.query_params['forecast_id'])
			print("DB reached")
			serializer = SlideForecastImageSerializer(slides,context={'request':request},many=True)
			content = serializer.data
		return Response(content,status=status_return)
	def create(self, request):
		status_return = status.HTTP_200_OK
		slides_data = request.data
		print(slides_data)
		result_slides = []
		slides_forecast_id = slides_data[0]['forecast_id']
		#slides_forecast_id = RegionalForecast.objects.get(taxonomy_id = slides_data[0]['forecast_id']).pk
		SlideForecastImage.objects.filter(forecast_id = slides_forecast_id).delete()
		#Para evitar problemas a la hora de devolver slides, estos se devuelven unicamente cada 6h
		for slide in slides_data:
			if datetime.datetime.strptime(slide["date"],"%Y-%m-%dT%H:%M:%S").hour % 6 == 0:
				result_slides.append(slide)
		print(result_slides)
		# for slide_data in slides_data:
		#     slide_data['forecast_id'] = slides_forecast_id
		serialize_data = SlideForecastImageSerializer(data =result_slides, many=True)
		if serialize_data.is_valid():
			serialize_data.save()
			logger.debug('Slides data updated')
			content = {'Slides data added'}
		else:
			logger.error(serialize_data.errors)
			status_return = status.HTTP_404_NOT_FOUND
			content = {'Message':'Wrong slides data format'}
		return Response(content, status=status_return)


class LanguageViewSet(ModelViewSet):
	queryset = Language.objects.all()
	serializer_class = LanguageSerializer

class LocalForecastTranslationViewSet(ModelViewSet):
	queryset = LocalForecastTranslation.objects.all()
	serializer_class = LocalForecastTranslationSerializer
