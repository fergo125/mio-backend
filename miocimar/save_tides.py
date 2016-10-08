from api.models import TideEntry, TideRegion
import json
import os

data = []

regions = [{
	"name": "Bahia Culebra",
	"file": "bahia_culebra"
}, {
	"name": "Bahia Uvita",
	"file": "bahia_uvita"
}, {
	"name": "Golfito",
	"file": "golfito"
}, {
	"name": "Golfo Elena",
	"file": "golfo_elena"
}, {
	"name": "Isla del Coco",
	"file": "isla_coco"
}, {
	"name": "Puerto Herradura",
	"file": "puerto_herradura"
}, {
	"name": "Quepos",
	"file": "quepos"
}, {
        "name": "Puntarenas",
        "file": "puntarenas"
}, {
        "name": "Limon",
        "file": "limon"
}]

if TideRegion.objects.count() != 0:
	TideRegion.objects.all().delete()
	TideEntry.objects.all().delete()

for region_data in regions:
	region = TideRegion(name=region_data["name"])
	region.save()

	with open('../tide_files/{0}.tides.json'.format(region_data["file"])) as data_file:
		data = json.load(data_file)
		entry_list = []
		for record in data:
			entry = TideEntry(\
				tide_region = region,\
			    date = record["date"] + "-06:00",\
			    tide_height = record["height"],\
			    is_high_tide = record["is_high"],\
			    moon = record["moon"])
			entry_list.append(entry)
		TideEntry.objects.bulk_create(entry_list)

print "Finished"

