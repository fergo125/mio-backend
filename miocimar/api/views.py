from django.shortcuts import render
from api.models import *
from api.serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import datetime

class TideWeek(APIView):
    """docstring for TideWeek"""
    def get(self, request, pk, format=None):
        start_date = datetime.date.today() - datetime.timedelta(days=1)
        end_date = datetime.date.today() + datetime.timedelta(days=7)
        tides = TideEntry.objects \
            .filter(date__gt=start_date) \
            .filter(date__lt=end_date) \
            .filter(tide_region=pk)
        serializer = TideEntrySerializer(tides, many=True)
        return Response(serializer.data)

class LocalForecastList(APIView):
    """docstring for LocalForecastList"""
    def get(self, request, format=None):
        localForecast = LocalForecast.objects.all()
        serializer = LocalForecastSerializer(localForecast,many=True)
        return Response(serializer.data)
# Create your views here.
