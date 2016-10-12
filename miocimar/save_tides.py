from api.models import TideEntry, TideRegion
import json
import os

data = []

regions = [{
    "name": "Puntarenas",
    "file": "puntarenas"
}]
'''
if TideRegion.objects.count() != 0:
    TideRegion.objects.all().delete()
    TideEntry.objects.all().delete()
'''
for region_data in regions:
    TideEntry.objects.filter(tide_region_id=42).delete()
    region = TideRegion.objects.get(pk=42) #(name=region_data["name"])
    #region.save()

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

