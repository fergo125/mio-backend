import requests

api_base = "https://mio-cimar.herokuapp.com"

# Get regions
r = requests.get("{0}/api/local_forecasts/".format(api_base))

regions = r.json()["results"]

for region in regions:
	# Get data from API's weekly view endpoint
	r = requests.get("{0}/api/local_forecasts/{1}/weekly_view/".format(api_base, region["id"]))
	data_list = r.json()

	for data in data_list:
		# Revelant values, rounded to 1 decimal only
		V = round(data["wind_speed"], 1)
		Hs = round(data["wave_height_sig"], 1)
		T = round(data["wave_period"], 1)

		isCaribbean = region["name"] == "Caribe"

		error = False

		if not (
			# Second card thresholds
			(V >= 40 and Hs > 1.7) or
			(V >= 30.0 and Hs >= 2.0) or
			(V >= 40.0 and 1 < Hs <= 1.7) or
			(25 <= V < 40 and 1.2<= Hs < 2.0) or
			(25 < V < 30 and Hs >= 2.0) or
			(0 <= V <= 25 and 1 <= Hs <= 3.0) or
			(0 <= V <= 25 and Hs < 1)):
			error = True
		if not isCaribbean:
			# First and third card thresholds for non caribbean
			if not ((Hs > 2.3 and T >= 15) or
				(1.7 < Hs <= 2.3 and T >= 15) or
				(1.0 <= Hs <= 1.7 and T >= 15) or
				(0.75 <= Hs < 2.5 and T < 15) or
				(Hs < 0.75 and T < 15)):
				error = True
		else:
			# First and thid card thresholds for caribbean
			if not ((Hs >= 3.0) or
					(2.3 < Hs < 3.0) or
					(1.5 <= Hs <= 2.3) or
					(0.75 <= Hs < 1.5) or
					(Hs < 0.75)):
				error = True

		if error:
			print("Threshold error: V = {0}, Hs = {1}, T = {2}, on {3}, {4}".format(V, Hs, T, region["name"].encode("utf-8"), data["date"]))
