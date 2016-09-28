#!/usr/bin/python

import argparse
import json
from datetime import datetime
import dateutil.parser

parser = argparse.ArgumentParser()
parser.add_argument('file')
args = parser.parse_args()


DATE_FORMAT = "%B %d, %Y %H:%M"

def value_for_moon_code(moon_code):
    return {
        "NM": 1,
        "1Q": 9,
        "FM": 17,
        "3Q": 25
    }[moon_code]

def offsets_for_day_diff(days):
    return {
        5: [1,    3,    5,    7],
        6: [1, 2,    4,    6, 7],
        7: [1, 2, 3,    5, 6, 7],
        8: [1, 2, 3, 4, 5, 6, 7],
        9: [1, 2, 3,4,4, 5, 6, 7]
    }[days]

file_lines = open(args.file, "r").readlines()

temp_counter = 0

# Counters for "same day records"
last_date_processed = None
days_between_moons = []
same_day_counter = 1
diff_days_counters = []

results = []

# Pointer to last day with declared moon
last_date_with_moon = None
last_date_with_moon_index = 0

last_height = 0

try:
    for line in file_lines:
        line_parts = line.split()
        if line_parts[0] == "Septembe":
            line_parts[0] = "September"
        if len(line_parts) not in [5, 6]:
            continue

        b = line_parts
        s = "{0} {1} {2} {3}".format(line_parts[0], line_parts[1], line_parts[2], line_parts[3])
        d = datetime.strptime(s, DATE_FORMAT)

        height = line_parts[4]
        is_high = height > last_height
        last_height = height
        o = {
            "date": d.isoformat(),
            "height": float(height),
            "is_high": is_high
        }

        # Same-day records counter
        '''
        if last_date_processed is not None:
            if d.replace(minute=0, hour=0) == last_date_processed.replace(minute=0, hour=0):
                same_day_counter += 1
            else:
                # Just lost same day record
                if same_day_counter not in diff_days_counters:
                    print "Starting new day, counter was at "+str(same_day_counter) + ", for days: " + d.isoformat() + " and " + last_date_processed.isoformat()
                    diff_days_counters.append(same_day_counter)
                same_day_counter = 1
        last_date_processed = d
        '''

        # Moon calculations
        if len(b) > 5:
            o["moon"] = value_for_moon_code(line_parts[5])

            if last_date_with_moon is not None:
                difference = d.replace(hour=0, minute=0) - last_date_with_moon.replace(hour=0, minute=0)
                if difference.days > 0:
                    #print "Should fill moons from index {0} to {1}".format(last_date_with_moon_index, len(results))
                    offsets = offsets_for_day_diff(difference.days)
                    for x in range(last_date_with_moon_index + 1, len(results)):
                        # Check days with no moons between current and last one, and fill their moons
                        x_date = dateutil.parser.parse(results[x]["date"])

                        # Offset in days between this date and the last moon
                        offset = (x_date.replace(hour=0, minute=0) - last_date_with_moon.replace(hour=0, minute=0)).days

                        # Calculate last moon's code
                        last_moon = o["moon"] - 8 if o["moon"] != 1 else 25
                        x_moon = last_moon + offsets[offset - 1]
                        results[x]["moon"] = x_moon
                    '''
                    if difference.days not in days_between_moons:
                        print "Difference between " + last_date_with_moon.replace(hour=0, minute=0).isoformat() + " and " + d.replace(hour=0, minute=0).isoformat()
                        days_between_moons.append(difference.days)'''
            else:
                # Do something for the first records (there's no previous moon)
                for x in range(0, len(results)):
                    x_date = dateutil.parser.parse(results[x]["date"])
                    offset = (d.replace(hour=0, minute=0) - x_date.replace(hour=0, minute=0)).days
                    results[x]["moon"] = o["moon"] - offset
            last_date_with_moon = d
            last_date_with_moon_index = len(results)

        results.append(o)

        '''temp_counter += 1
        if temp_counter == 200:
            break'''
except:
    pass
finally:
    # Write results to json file with 'pretty' format
    open(args.file + ".json", "w").write(json.dumps(results, indent=2, separators=(',', ': ')))

# print days_between_moons
# print diff_days_counters
