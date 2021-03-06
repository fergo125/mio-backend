import csv
import json
import math
import datetime
import requests
import sys
import os
import api.serializers as serializers
import tempfile
#sys.path.append(os.path.join('..','..'))
from csv_utilities import FileUtilities
from csv_utilities import CSVProcessor
from api.models import LocalForecast, LocalForecastEntry, RegionalForecast, WaveWarning
import dateutil.parser
import pytz

paths={'text':['body','und','value'],
'csv_file':['field_csv','und','filename'],
'gif_file':['field_imagen_movil','und','filename'],
'date':['field_fecha','und','value'],
'element_type':['type'],
'local_forecast_taxonomy_id':['field_taxonomia_oleaje_viento','und','tid'],
'regional_forecast_taxonomy_id':['field_taxonomia_regional','und','tid'],
'title':['title'],
'level':['field_tipo_de_alerta','und','value'],
'subtitle':['field_subtitle','und','value'],
'notification':['field_notificacion','und','value']
}


data_path_local={'text','csv_file','date','element_type','local_forecast_taxonomy_id'}
data_path_regional={'text','date','gif_file','regional_forecast_taxonomy_id'}
data_path_warning={'text','level','date','title','subtitle','notification'}

localArrayProcess={}

API_DIR= r"http://miocimar.ucr.ac.cr/"
LOCAL_FORECAST_TYPE = r"pronostico_oleaje_y_viento"
FIREBASE_URL="https://fcm.googleapis.com/fcm/send"

FIREBASE_KEY = "AIzaSyB34V3DG892dzg9gXnneVz8-i1bvuQUuBk"
#testid = 1397
def getNodeData(node_id):
	#conseguir los datos del nodo
	node_dir= API_DIR + r"api/node/" + str(node_id) +".json"
	node = requests.get(node_dir)
	if node.status_code == 200:
		node_list = json.loads(node.text)
		return node_list
	else:
		return None
	#ya se logran descargar los datos del pronostico correctamente resta lograr darle forma y salvarlos en el base de datos
	#desmenusar los datos en los parametros que necesitamos par el modelo

	#Revisar el modelo de datos que hay en el e
def getParam(path, data):
	for i in path:
		if i in data:
			data = data[i]
			if type(data) is list:
				data = data[0]
		else:
			return None
	return data

def getNodeTaxonomyID(data):
	node_type = getParam(paths['element_type'],data)
	tax_id=0
	if node_type == LOCAL_FORECAST_TYPE:
		tax_id = getParam(paths['local_forecast_taxonomy_id'],data  )
	return tax_id

#TODO add another types of messages to return for the following cases:
#the csv where not found, the csvs couldnt be decoded, the node wasn't found
def localForecastUpdate(node_id):
	#The API does a request to the drupal webpage to get node content.
	node_data = getNodeData(node_id)
	if node_data is None:
		return False
	#Gets the tax_id to see what kind of content is.
	tax_id = getNodeTaxonomyID(node_data)
	model_data_dict = dict()

	file_utilities = FileUtilities()
	csv_processor = CSVProcessor()
	#Using the path vector declared above, the attributes of interest
	#are collected from json data downloaded from the content publication.
	#Each kind of content has the data paths necessary according to its model.
	for i in data_path_local:
		model_data_dict[i]=getParam(paths[i],node_data)

	if model_data_dict['csv_file'] is not None:
		file_name = model_data_dict['csv_file']
		file_url = API_DIR+'sites/default/files/csvs/'+file_name
		csv_data_json = None

		# TODO: Change to get a string and pass it as an array
		csv_content = requests.get(file_url).text
		print "File url is " + file_url
		print "CSV Downloaded"
		print "File size is " + str(len(csv_content))
		csv_lines = csv_content.splitlines()
		print "Total csv lines is " + str(len(csv_lines))
		my_local_forecast = LocalForecast.objects.get(taxonomy_id=model_data_dict['local_forecast_taxonomy_id'])
		print "Using region with id " + str(my_local_forecast.pk)
		csv_data_json = csv_processor.processData(csv_lines, my_local_forecast.pk)
		if csv_data_json is not None:
			print "Processed CSV Data is not none"
			print "Len is " + str(len(csv_data_json))
			saveLocalForecastEntries(csv_data_json)
		else:
			print "CSV Data is none"
	if model_data_dict['text'] is not None:
		updateLocalForecastText(model_data_dict['text'],model_data_dict['local_forecast_taxonomy_id'])
	return True

def proces_csv_parameters(filename,taxonomy_id=None,localforecast_id = None):
	csv_processor = CSVProcessor()
	file_url = API_DIR+'sites/default/files/csvs/'+filename
	csv_data_json = None

	# TODO: Change to get a string and pass it as an array
	csv_content = requests.get(file_url).text
	print "File url is " + file_url
	print "CSV Downloaded"
	print "File size is " + str(len(csv_content))
	csv_lines = csv_content.splitlines()
	print "Total csv lines is " + str(len(csv_lines))
	local_forecast_pk= localforecast_id
	if taxonomy_id is not None:
   		local_forecast_pk = LocalForecast.objects.get(taxonomy_id=model_data_dict['local_forecast_taxonomy_id']).pk
	print "Using region with id " + str(local_forecast_pk)
	csv_data_json = csv_processor.processData(csv_lines, local_forecast_pk)
	if csv_data_json is not None:
		print "Processed CSV Data is not none"
		print "Len is " + str(len(csv_data_json))
		saveLocalForecastEntries(csv_data_json)
	else:
		print "CSV Data is none"
	return True

def saveLocalForecastEntries(data_json):
	print "Saving local forecast entries"
	serialized_list = serializers.LocalForecastEntryCreateSerializer(data=data_json, many=True)
	if serialized_list.is_valid():

		#Run one by one each new object
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
				update_entry = serializers.LocalForecastEntryCreateSerializer(existing_entry, data=serialized_object)
				if update_entry.is_valid():
					update_entry.save()
				else:
					# TODO: Update this to a logging statement later
					print("Couldn't serialize and update this entry: ", str(serialized_object))
			else:

				# There was no previous object
				new_entry = serializers.LocalForecastEntryCreateSerializer(data=serialized_object)
				if new_entry.is_valid():
					new_entry.save()
				else:
					# TODO: Update this to a logging statement later
					print ("Couldn't serialize and create this entry: " , str(serialized_object))
	else:
		print "Serialized list is invalid"
		print serialized_list.errors

def updateLocalForecastText(new_text,forecast_id):
	localForecast = LocalForecast.objects.get(taxonomy_id=forecast_id)
	if localForecast is not None:
		localForecast.comment = new_text
		localForecast.save()
	else:
		print("No entry avaiable")

def regionalForecastUpdate(node_id):
	node_data = getNodeData(node_id)
	if node_data is None:
		return False
		#Gets the tax_id to see what kind of content is.
	model_data_dict = dict()
	#Using the path vector declared above, the attributes of interest
	#are collected from json data downloaded from the content publication.
	#Each kind of content has the data paths necessary according to its model.
	for i in data_path_regional:
		model_data_dict[i]=getParam(paths[i],node_data)
	latest_forecast = RegionalForecast.objects.get(taxonomy_id=model_data_dict['regional_forecast_taxonomy_id'])
	if latest_forecast is not None:
		date_as_string = model_data_dict["date"]
		print date_as_string
		latest_forecast.date = pytz.utc.localize(dateutil.parser.parse(date_as_string)).isoformat()
		print latest_forecast.date
		latest_forecast.text = model_data_dict["text"]
		latest_forecast.animation_url = API_DIR + "sites/default/files/gifs/" + model_data_dict["gif_file"]
		latest_forecast.save()
	else:
		return False
	return True

def warningUpdate(node_id):
	node_data = getNodeData(node_id)
	if node_data is None:
		return False
		#Gets the tax_id to see what kind of content is.
	model_data_dict = dict()
	#Using the path vector declared above, the attributes of interest
	#are collected from json data downloaded from the content publication.
	#Each kind of content has the data paths necessary according to its model.
	for i in data_path_warning:
		model_data_dict[i]=getParam(paths[i],node_data)
	try:
		warning = WaveWarning.objects.get(pk=int(node_id))
	except:
		warning = WaveWarning(pk=int(node_id))
	warning.level = getWarningType(model_data_dict["level"])
	date_as_string = model_data_dict["date"]
	warning.date = pytz.utc.localize(dateutil.parser.parse(date_as_string)).isoformat()
	warning.text = model_data_dict["text"]
	warning.title = model_data_dict["title"]
	warning.subtitle = model_data_dict["subtitle"]
	warning.save()
	if int(model_data_dict['notification']):
		sendNewNotification(node_id)
	return True

def getWarningType(warning_type):
	if warning_type == "verde":
		return 0
	if warning_type == "amarilla":
		return 1
	if warning_type == "roja":
		return 2

def sendNewNotification(notification_id):
	notification_object = WaveWarning.objects.get(id=int(notification_id))

	access_key = 'key='+FIREBASE_KEY
	request_headers = {'Content-Type':'application/json','Authorization':access_key}

	# Android body
	request_body_android = {
		"to": "/topics/notifications",
		"priority" : "high",
		"data": {
			"title": notification_object.title,
			"subtitle": notification_object.subtitle,
			"notificationId": str(notification_id),
			"notificationLevel": str(notification_object.level)
		}
	}
	encoded_android_request = json.dumps(request_body_android).encode('utf-8')

	# iOS body
	request_body_ios = {
		"to": "/topics/notificationsios",
		"content_available": True,
		"priority" : "high",
		"notification": {
			"title": notification_object.title,
			"body": notification_object.subtitle,
			"sound": "default"
		},
		"data": {
			"notificationId": str(notification_id),
			"notificationLevel": str(notification_object.level)
		}
	}
	encoded_ios_request = json.dumps(request_body_ios).encode('utf-8')


	response = requests.post(FIREBASE_URL,data=encoded_ios_request,headers=request_headers)
	response = requests.post(FIREBASE_URL,data=encoded_android_request,headers=request_headers)
