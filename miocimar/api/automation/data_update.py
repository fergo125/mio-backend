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
from api.models import LocalForecast,RegionalForecast,WaveWarning


paths={'text':['body','und','value'],
'csv_file':['field_csv','und','filename'],
'gif_file':['field_gif','und','filename'],
'date':['field_fecha','und','value'],
'element_type':['type'],
'local_forecast_taxonomy_id':['field_taxonomia_oleaje_viento','und','tid'],
'regional_forecast_taxonomy_id':['field_taxonomia_regional','und','tid'],
'title':['title'],
'level':['field_tipo_de_alerta','und','value']
}


data_path_local={'text','csv_file','date','element_type','local_forecast_taxonomy_id'}
data_path_regional={'text','date','gif_file','regional_forecast_taxonomy_id'}
data_path_warning={'text','level','date','title'}

localArrayProcess={}

API_DIR= r"http://miocimar-test.ucr.ac.cr/"
LOCAL_FORECAST_TYPE = r"pronostico_oleaje_y_viento"
FIREBASE_URL="https://fcm.googleapis.com/fcm/send"

FIREBASE_KEY = "key=AIzaSyB34V3DG892dzg9gXnneVz8-i1bvuQUuBk"
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
        with tempfile.TemporaryFile() as csv_file:
            if file_utilities.downloadFile(file_url,csv_file):
                csv_data_json = csv_processor.processData(csv_file,model_data_dict['local_forecast_taxonomy_id'])
                if csv_data_json is not None:
                    saveLocalForecastEntries(csv_data_json)
    if model_data_dict['text'] is not None:
        updateLocalForecastText(model_data_dict['text'],model_data_dict['local_forecast_taxonomy_id'])
    return True


def saveLocalForecastEntries(data_json):
    serialized_list = serserializers.LocalForecastEntry(data=data_json, many=True)
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
                update_entry = LocalForecastEntryCreateSerializer(existing_entry, data=serialized_object)
                if update_entry.is_valid():
                    update_entry.save()
                else:
                    # TODO: Update this to a logging statement later
                    print("Couldn't serialize and update this entry: ", str(serialized_object))
            else:

                # There was no previous object
                new_entry = LocalForecastEntryCreateSerializer(data=serialized_object)
                if new_entry.is_valid():
                    new_entry.save()
                else:
                    # TODO: Update this to a logging statement later
                    print ("Couldn't serialize and create this entry: " , str(serialized_object))

def updateLocalForecastText(new_text,forecast_id):
    localForecast = LocalForecast.objects.get(pk=forecast_id)
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
    latest_forecast = RegionalForecast.objects.get(id=model_data_dict['regional_forecast_taxonomy_id'])
    if latest_forecast is not None:
        string_datetime =  datetime.datetime.strptime(model_data_dict["date"],'%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        string_datetime += "Z"
        #latest_forecast.date = datetime.datetime.strptime(model_data_dict["date"],'%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        latest_forecast.date = string_datetime
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
    warning.date = datetime.datetime.strptime(model_data_dict["date"],'%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')+"Z"
    warning.text = model_data_dict["text"]
    warning.title = model_data_dict["title"]
    warning.save()
    sendNewNotification(node_id)
    return True

def getWarningType(warning_type):
    if warning_type == "amarilla":
        return 1
    if warning_type == "roja":
        return 2

def sendNewNotification(notification_id):
    notification_object = WaveWarning.objects.get(id=int(notification_id))
    print(notification_object)
    access_key = 'key='+FIREBASE_KEY
    request_body = r'{ "to": "/topics/notifications","data": {"title": "'+notification_object.title+'","subtitle": "'+notification_object.subtitle+'","notificationId": "'+str(notification_id)+'","notificationLevel": "'+str(notification_object.level)+'"}}'
    request_headers = {'Content/type':'application/json','Authorization':access_key}
    request_body_encoded = request_body.encode('utf-8')
    print(request_body_encoded)
    response = requests.post(FIREBASE_URL,data=request_body_encoded,headers=request_headers)
    print(response)
