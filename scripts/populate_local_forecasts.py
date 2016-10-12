# Indicate URL to point to

URL = 'http://localhost:8000/api/'

WEEKS_BEFORE = 2
WEEKS_AFTER = 4

import json
import requests
from datetime import datetime, timedelta
import random

region_count = requests.get(URL + 'local_forecasts/').json()['count']

sample_count = (WEEKS_BEFORE + 1 + WEEKS_AFTER) * 7 * 4
samples = []
start_date = datetime.utcnow() - timedelta(weeks=WEEKS_BEFORE)

for region in range(0, region_count):
    for counter in range(0, sample_count):
        date = start_date + timedelta(hours=counter*6)
        sample = {
            "wind_speed": random.uniform(0.5, 60.0),
            "wave_period": random.uniform(10.0, 50.0),
            "wave_height_max": random.uniform(1.0, 5.0),
            "local_forecast": region + 1,
            "wind_burst": random.uniform(10.0, 50.0),
            "wind_direction": random.uniform(-100.0, 100.0),
            "wave_height_sig": random.uniform(0.0, 4.0),
            "date": date.isoformat(),
            "wave_direction": random.uniform(-100.0, 100.0)
        }
        samples.append(sample)
print samples[0]
print "Sending {0} samples into local forecasts.".format(len(samples))
response = requests.post(URL + 'local_forecast_entry/', data=json.dumps(samples), headers={'Content-Type': 'application/json'})
print "Result message: {0}".format(response.json()['message'])
