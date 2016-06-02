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
    def get(self, request,pk, format=None):
        end_date = datetime.date.today() + datetime.timedelta(days=8)
        #tides = TideEntry.objects.all()
        tides = TideEntry.objects.filter(date__gt=datetime.date.today()).filter(date__lt=end_date).filter(tide_region=pk)
        serializer = TideEntrySerializer(tides,many=True)
        return Response(serializer.data)
# Create your views here.
