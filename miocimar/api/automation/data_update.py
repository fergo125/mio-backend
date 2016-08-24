import csv
import json
import math
import datetime
import requests
import sys
import os

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

API_DIR= r"http://miocimar-test.ucr.ac.cr/api/"
LOCAL_FORECAST_TYPE = r"pronostico_oleaje_y_viento"
#testid = 1397
def getNodeData(node_id):
    #conseguir los datos del nodo
    node_dir= API_DIR + r"node/" + str(node_id) +".json"
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
    print(model_data_list)

def regionalForecastUpdate():
    pass

def warningUpdate():
    pass
