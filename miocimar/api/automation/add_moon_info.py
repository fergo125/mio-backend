import argparse
import json
from datetime import datetime
import dateutil.parser

parser = argparse.ArgumentParser()
parser.add_argument('file_with_moon')
parser.add_argument('file_without_moon')
args = parser.parse_args()

file_with_moon = open(args.file_with_moon)
file_without_moon = open(args.file_without_moon)

def are_same_day(date1, date2):
	return (wom_date.replace(hour=0, minute=0) - wm_date.replace(hour=0, minute=0)).days == 0

wom = 0
wm = 0

wom_data = json.load(file_without_moon)
wm_data = json.load(file_with_moon)

last_wom_date = None
last_moon = 0

# len(wom_data)
for wom in range(0, len(wom_data)):

	wom_date = dateutil.parser.parse(wom_data[wom]["date"])

	# If it's the same day for the wom, just set the same moon
	if (last_wom_date is not None and are_same_day(wom_date, last_wom_date)):
		wom_data[wom]["moon"] = last_moon
		continue

	is_same_day = False
	while not is_same_day:
		wm += 1
		wm_date = dateutil.parser.parse(wm_data[wm]["date"])
		is_same_day = are_same_day(wom_date, wm_date)

	last_moon = wm_data[wm]["moon"]
	wom_data[wom]["moon"] = last_moon

	last_wom_date = wom_date

open("newfile.json", "w").write(json.dumps(wom_data, indent=2, separators=(',', ': ')))
