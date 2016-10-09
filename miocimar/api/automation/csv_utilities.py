import csv
import json
import math
import datetime
import requests
import sys
import os
import dateutil.parser
import pytz

cr_timezone = pytz.timezone('America/Costa_Rica')

#Time,sig_wav_ht_surface,max_wav_ht_surface,peak_wav_dir_surface,peak_wav_per_surface,u-component_of_wind_height_above_ground,v-component_of_wind_height_above_ground

# def main():
# 	# gatherer = FileGatherer()
# 	processor = CSVProcessor()
# 	APIDIR="http://localhost:8000/api/local_forecast_entry/"
#
# 	# filesToDownload = gatherer.fileList()
# 	# filenames =gatherer.fileToArray(filesToDownload)
# 	# API_ROOT=""
# 	# filenames = gatherer.fileToArray('allentries.json')
# 	# if gatherer.fileDownloader(filenames):
# 	# 	print("Archios descargados satisfactoriamente")
# 	# else:
# 	# 	print("no se pudo descargar los archivos")
# 	for fn in os.listdir("csvs/"):
# 		filedir = "csvs/"+fn
# 		if os.path.isfile(filedir):
# 			data=''
#
# 			if fn[0:2] == "ca":
# 				data = processor.processData(filedir,7)
# 			if fn[0:2] == "cp":
# 				data = processor.processData(filedir,2)
# 			if fn[0:2] == "ic":
# 				data = processor.processData(filedir,8)
# 			if fn[0:2] == "np":
# 				data = processor.processData(filedir,1)
# 			if fn[0:2] == "pc":
# 				data = processor.processData(filedir,5)
# 			if fn[0:2] == "pu":
# 				data = processor.processData(filedir,4)
# 			if fn[0:2] == "sp":
# 				data = processor.processData(filedir,3)
# 			if fn[0:2] == "ps":
# 				data = processor.processData(filedir,6)
# 			print(data)
# 			processor.publishData(APIDIR,data)
#

	# date
    # wave_height_sig
    # wave_height_max=1.3*wave_height_sig
    # wave_direction
    # wave_period
    # wind_direction
    # wind_speed= sqrt(pow(u,2) + pow(u,2))
    # wind_burst= wind_speed*1.3

class FileUtilities:
	def fileList(self):
		pageNumber = 0
		listResult = 'empty array'
		#fileList
		allentries = list()
		pythonlist ='a'
		filename='allentries.json'
		while pythonlist:
			filelist_get_url = 'http://miocimar.ucr.ac.cr/api/file?page='+str(pageNumber)+'&fields=filename&parameters[filemime]=text/csv'
			print(filelist_get_url)
			request_result = requests.get(filelist_get_url)
			pythonlist = json.loads(request_result.text)
			print(request_result)
			#print(pythonlist)
			#print(pythonlist)
			if pythonlist:
				allentries.extend(pythonlist)
			pageNumber+=1
		with open(filename,'wb') as f:
			f.truncate()
			f.write(json.dumps(allentries))
		return	filename

	def downloadFile(self,url,f):
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
					#sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)))
					#sys.stdout.flush()
			return True
		else:
			return False

	def fileDownloader(self,files):
		FILEROOT= "http://miocimar.ucr.ac.cr/sites/default/files/csvs/"
		for filename in files:
			print(filename)
			filedir = "csvs/"+filename
			with open(filedir,"wb") as f:
				url = FILEROOT + filename
				if not self.downloadFile(url, f):
					print("No se pudo descargar el archivo:",filename)
		return True
	def fileToArray(self,filename):
		with open(filename,"r") as filenames:
			array= json.loads(filenames.read())
			newArray = list()
			for element in array:
				newArray.append(element["filename"])
			return newArray

class CSVProcessor:
	"""
	Recibe el nombre del archivo en que se descargo el csv y ID del pronostico del cual se van a sacar los datos
	de los archivos, el script tiene los campos de los datos en los cuales
	"""
	def processData(self, array_of_lines, forecastID):
		fn = ['date','wave_height_sig','wave_height_max','wave_direction','wave_period','u-component_of_wind_height_above_ground','v-component_of_wind_height_above_ground']
		data= list()
		print "Will read with DictReader"
		readerCSV = csv.DictReader(array_of_lines,fieldnames=fn)
		print "Did read with DictReader"
		for rue in readerCSV:
			data.append(rue)
		print "Len of data is " + str(len(data))
		if data:
			del data[0]
			newData = self.makeWindData(data,forecastID)
			return newData
		else:
			print "Will return none from processData"
			return None

	# And also fix the wave direction
	def makeWindData(self, dataList, forecastID):
		newDataList = list()
		for rue in dataList:
			# Correction to the wave direction
			rue['wave_direction'] = float(rue['wave_direction'])
			rue['wave_direction'] -= 180
			if rue['wave_direction'] < 0:
				rue['wave_direction'] += 360

			u_wind_component = float(rue['u-component_of_wind_height_above_ground'])
			v_wind_component = float(rue['v-component_of_wind_height_above_ground'])

			rue['date'] = self.newDateFormat(rue['date'])
			if u_wind_component is not None and v_wind_component is not None:
				rue['wind_speed'] = self.windSpeedFromTwoComponents(u_wind_component,v_wind_component)
				rue['wind_direction'] = self.windDirectionFromTwoComponents(u_wind_component,v_wind_component)
			else:
				rue['wind_speed'] = None
				rue['wind_direction'] = None

			if rue['wind_speed'] is not None:
				wind_speed = float(rue['wind_speed'])
				rue['wind_burst'] = wind_speed*1.3
			else:
				rue['wind_burst'] = None
			rue['local_forecast'] = forecastID
			del rue['u-component_of_wind_height_above_ground']
			del rue['v-component_of_wind_height_above_ground']
			newDataList.append(rue)
		return newDataList

	def publishData(self,destiny,jsonData):
		headers={'content-type':'application/json','Accept':'application/json'}
		response =requests.post(destiny,jsonData,headers=headers)
		print(response.content)

	def windSpeedFromTwoComponents(self,u,v):
		return math.sqrt(pow(u, 2) + pow(v, 2)) * 3.6

	def windDirectionFromTwoComponents(self,u,v):
		return math.atan2(u, v) * (180 / math.pi)

	def newDateFormat(self,date_as_string):
		return cr_timezone.localize(dateutil.parser.parse(date_as_string)).isoformat()
#
# if __name__== "__main__":
# 	main()
