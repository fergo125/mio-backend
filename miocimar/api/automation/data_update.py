import csv
import json
import math
import datetime
import requests
import sys
import os
import api.serializers as serializers
#sys.path.append(os.path.join('..','..'))
from csv_utilities import FileUtilities as file_utilities
from csv_utilities import CSVProcessor as csv_processor
from api.models import LocalForecast


paths={'text':['body','und','value'],
'csv_file':['field_csv','und','filename'],
'gif_file':['field_gif','und','filename'],
'date':['field_fecha','und','value'],
'element_type':['type'],
'local_forecast_taxonomy_id':['field_taxonomia_oleaje_viento','und','tid'],
'regional_forecast_taxonomy_id':['field_taxonomia_regional','und','tid'],
}

data_path_local={'text','csv_file','date','element_type','local_forecast_taxonomy_id'}
data_path_regional={'text','date','element_type'}
data_path_warning={}

localArrayProcess={}

API_DIR= r"http://miocimar-test.ucr.ac.cr/"
LOCAL_FORECAST_TYPE = r"pronostico_oleaje_y_viento"

#testid = 1397
def getNodeData(node_id):
    #conseguir los datos del nodo
    node_dir= API_DIR + r"api/node/" + str(node_id) +".json"
    print(node_dir)
    node = requests.get(node_dir)
    node_list = json.loads(node.text)
    print("All nodes:")
    print(node_list)
    return node_list
    #ya se logran descargar los datos del pronostico correctamente resta lograr darle forma y salvarlos en el base de datos
    #desmenusar los datos en los parametros que necesitamos par el modelo

    #Revisar el modelo de datos que hay en el e
def getParam(path, data):
    for i in path:
        print("Data navigation with i="+i+":")
        data = data[i]
        if type(data) is list:
            data = data[0]
            print(data)
        print(data)
    return data

def getNodeTaxonomyID(data):
    node_type = getParam(paths['element_type'],data)
    tax_id=0
    if node_type == LOCAL_FORECAST_TYPE:
        tax_id = getParam(paths['local_forecast_taxonomy_id'],data  )
    return tax_id


def localForecastUpdate(node_id):
    node_data = getNodeData(node_id)
    tax_id = getNodeTaxonomyID(node_data)
    model_data_list = list()
    for i in data_path_local:
        model_data_list.append({i:getParam(paths[i],node_data)})
    file_name = model_data_list[1]
    file_url = API_DIR+'sites/default/files/csvs/'+file_name
    csv_file = file()
    file_utilities.downloadFile(file_url,csv_file)
    csv_data_json = csv_processor.processData(csv_file,tax_id)
    serialized_list = serserializers.LocalForecastEntry(data=csv_data_json, many=True)
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
    print(model_data_list)

def regionalForecastUpdate():
    pass

def warningUpdate():
    pass

def downloadFile(url,f):
    f.truncate()
    response = requests.get(url,stream=True)
    print('Codigo de estado:',response.status_code)
    if(response.status_code == 200):
        total_length = response.headers.get('content-length')
        if total_length is None: # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content():
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)))
                sys.stdout.flush()
        return True
    else:
        return False
