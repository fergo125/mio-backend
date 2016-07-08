from datetime import datetime, timedelta
from django.test import TestCase
from . import APIClientTestCase

class APITestCase(APIClientTestCase):
    def test_get_local_forecast_regions(self):
        response = self.client.get('/api/local_forecasts/')
        self.assertEqual(200, response.status_code)
        data = response.data
        self.assertEqual(data['count'], 8)
        self.assertEqual(len(data['results']), 8)

    def test_get_local_forecast_region_data(self):
        response = self.client.get('/api/local_forecasts/1/weekly_view/')
        self.assertEqual(200, response.status_code)
        data = response.data

    def test_create_local_forecast_entries(self):
        # Count initial forecast entries
        response = self.client.get('/api/local_forecast_entry/')
        self.assertEqual(200, response.status_code)
        data = response.data
        initial_count = data['count']

        # Assert create method works
        test_data = [{"wind_speed": 5.606513379281393, "wave_period": "17.52120018005371", "wave_height_max": "2.3046445846557617", "local_forecast": 1, "wind_burst": 7.288467393065811, "wind_direction": -110.38035232899507, "wave_height_sig": "1.772803544998169", "date": "2016-06-23 00:00", "wave_direction": "222.88746643066406"}, {"wind_speed": 7.498165092886742, "wave_period": "17.258399963378906", "wave_height_max": "2.3961658477783203", "local_forecast": 1, "wind_burst": 9.747614620752765, "wind_direction": -122.09426554927323, "wave_height_sig": "1.843204379081726", "date": "2016-06-23 06:00", "wave_direction": "223.18267822265625"}, {"wind_speed": 6.491244513181828, "wave_period": "17.042800903320312", "wave_height_max": "2.498605966567993", "local_forecast": 1, "wind_burst": 8.438617867136376, "wind_direction": -126.56106683557694, "wave_height_sig": "1.9220044612884521", "date": "2016-06-23 12:00", "wave_direction": "221.46710205078125"}, {"wind_speed": 6.611735272403924, "wave_period": "17.478403091430664", "wave_height_max": "2.565685749053955", "local_forecast": 1, "wind_burst": 8.595255854125101, "wind_direction": -123.11956146457646, "wave_height_sig": "1.973604440689087", "date": "2016-06-23 18:00", "wave_direction": "224.21348571777344"}, {"wind_speed": 9.65172946143116, "wave_period": "17.9856014251709", "wave_height_max": "2.734686851501465", "local_forecast": 1, "wind_burst": 12.547248299860508, "wind_direction": -119.89220677220673, "wave_height_sig": "2.103605270385742", "date": "2016-06-24 00:00", "wave_direction": "224.64149475097656"}, {"wind_speed": 10.545510366643853, "wave_period": "19.189208984375", "wave_height_max": "2.908367156982422", "local_forecast": 1, "wind_burst": 13.70916347663701, "wind_direction": -126.02975269017686, "wave_height_sig": "2.2372055053710938", "date": "2016-06-24 06:00", "wave_direction": "225.3102569580078"}, {"wind_speed": 6.787097856639323, "wave_period": "19.837600708007812", "wave_height_max": "2.8667666912078857", "local_forecast": 1, "wind_burst": 8.823227213631121, "wind_direction": -132.11569334335198, "wave_height_sig": "2.205204963684082", "date": "2016-06-24 12:00", "wave_direction": "225.5286407470703"}, {"wind_speed": 7.673526328422989, "wave_period": "18.855199813842773", "wave_height_max": "2.7523655891418457", "local_forecast": 1, "wind_burst": 9.975584226949886, "wind_direction": -122.65638305696672, "wave_height_sig": "2.117204189300537", "date": "2016-06-24 18:00", "wave_direction": "224.6734619140625"}, {"wind_speed": 9.53236891209873, "wave_period": "18.583599090576172", "wave_height_max": "2.7040066719055176", "local_forecast": 1, "wind_burst": 12.39207958572835, "wind_direction": -117.57999517592914, "wave_height_sig": "2.080005168914795", "date": "2016-06-25 00:00", "wave_direction": "224.36424255371094"}, {"wind_speed": 9.435637511493985, "wave_period": "17.85559844970703", "wave_height_max": "2.6223666667938232", "local_forecast": 1, "wind_burst": 12.26632876494218, "wind_direction": -122.06215782339271, "wave_height_sig": "2.017204999923706", "date": "2016-06-25 06:00", "wave_direction": "223.38107299804688"}, {"wind_speed": 5.134166230174465, "wave_period": "17.555999755859375", "wave_height_max": "2.4060449600219727", "local_forecast": 1, "wind_burst": 6.6744160992268045, "wind_direction": -119.02939028238525, "wave_height_sig": "1.8508038520812988", "date": "2016-06-25 12:00", "wave_direction": "223.12347412109375"}, {"wind_speed": 4.329761931913972, "wave_period": "17.371999740600586", "wave_height_max": "2.263563632965088", "local_forecast": 1, "wind_burst": 5.6286905114881645, "wind_direction": -90.00753130207515, "wave_height_sig": "1.741202712059021", "date": "2016-06-25 18:00", "wave_direction": "223.41705322265625"}, {"wind_speed": 6.672829320956588, "wave_period": "16.926199913024902", "wave_height_max": "2.159824252128601", "local_forecast": 1, "wind_burst": 8.674678117243564, "wind_direction": -115.58539349435614, "wave_height_sig": "1.6614031791687012", "date": "2016-06-26 00:00", "wave_direction": "222.39927673339844"}, {"wind_speed": 8.155490714010527, "wave_period": "16.48040008544922", "wave_height_max": "2.0560848712921143", "local_forecast": 1, "wind_burst": 10.602137928213686, "wind_direction": -116.08777127583438, "wave_height_sig": "1.5816036462783813", "date": "2016-06-26 06:00", "wave_direction": "221.38150024414062"}, {"wind_speed": 2.550115973988505, "wave_period": "16.277999877929688", "wave_height_max": "1.8668041229248047", "local_forecast": 1, "wind_burst": 3.3151507661850563, "wind_direction": -63.925138348532705, "wave_height_sig": "1.4360032081604004", "date": "2016-06-26 12:00", "wave_direction": "221.79190063476562"}, {"wind_speed": 0.7404821961727484, "wave_period": "15.685599327087402", "wave_height_max": "1.7139227390289307", "local_forecast": 1, "wind_burst": 0.9626268550245729, "wind_direction": -8.665437740062552, "wave_height_sig": "1.3184021711349487", "date": "2016-06-26 18:00", "wave_direction": "219.03829956054688"}, {"wind_speed": 5.290860120743055, "wave_period": "15.42039966583252", "wave_height_max": "1.6551626920700073", "local_forecast": 1, "wind_burst": 6.8781181569659715, "wind_direction": -115.8624429838522, "wave_height_sig": "1.2732020616531372", "date": "2016-06-27 00:00", "wave_direction": "219.43873596191406"}, {"wind_speed": 6.958499985813851, "wave_period": "15.181598663330078", "wave_height_max": "1.6556836366653442", "local_forecast": 1, "wind_burst": 9.046049981558006, "wind_direction": -120.3758964511021, "wave_height_sig": "1.2736027240753174", "date": "2016-06-27 06:00", "wave_direction": "219.901123046875"}, {"wind_speed": 6.028513926205934, "wave_period": "15.070416450500488", "wave_height_max": "1.6515231132507324", "local_forecast": 1, "wind_burst": 7.837068104067715, "wind_direction": -106.2785568677312, "wave_height_sig": "1.2704023122787476", "date": "2016-06-27 12:00", "wave_direction": "215.95872497558594"}, {"wind_speed": 0.013578113009966643, "wave_period": "17.47679901123047", "wave_height_max": "1.5854824781417847", "local_forecast": 1, "wind_burst": 0.017651546912956638, "wind_direction": -0.275436949478956, "wave_height_sig": "1.2196018695831299", "date": "2016-06-27 18:00", "wave_direction": "217.76466369628906"}, {"wind_speed": 4.836048083665388, "wave_period": "16.474401473999023", "wave_height_max": "1.6302025318145752", "local_forecast": 1, "wind_burst": 6.286862508765005, "wind_direction": -88.0705629177854, "wave_height_sig": "1.2540020942687988", "date": "2016-06-28 00:00", "wave_direction": "216.81988525390625"}, {"wind_speed": 5.9725105426038105, "wave_period": "16.21000099182129", "wave_height_max": "1.7113233804702759", "local_forecast": 1, "wind_burst": 7.764263705384954, "wind_direction": -122.62261972473407, "wave_height_sig": "1.3164026737213135", "date": "2016-06-28 06:00", "wave_direction": "217.3446807861328"}, {"wind_speed": 1.178893882970462, "wave_period": "15.584399223327637", "wave_height_max": "1.6978029012680054", "local_forecast": 1, "wind_burst": 1.5325620478616007, "wind_direction": -132.17490560194776, "wave_height_sig": "1.306002140045166", "date": "2016-06-28 12:00", "wave_direction": "216.443115234375"}, {"wind_speed": 3.5117745473153885, "wave_period": "15.33080005645752", "wave_height_max": "1.7269222736358643", "local_forecast": 1, "wind_burst": 4.565306911510005, "wind_direction": 30.643470243239644, "wave_height_sig": "1.3284016847610474", "date": "2016-06-28 18:00", "wave_direction": "217.12112426757812"}, {"wind_speed": 0.5877473698190292, "wave_period": "19.086000442504883", "wave_height_max": "1.7674823999404907", "local_forecast": 1, "wind_burst": 0.764071580764738, "wind_direction": 26.248772738598596, "wave_height_sig": "1.3596019744873047", "date": "2016-06-29 00:00", "wave_direction": "224.0674591064453"}, {"wind_speed": 2.454511074350757, "wave_period": "18.95800018310547", "wave_height_max": "1.85640287399292", "local_forecast": 1, "wind_burst": 3.1908643966559844, "wind_direction": -113.81406393126426, "wave_height_sig": "1.4280022382736206", "date": "2016-06-29 06:00", "wave_direction": "224.20266723632812"}, {"wind_speed": 3.1106997420891114, "wave_period": "18.405197143554688", "wave_height_max": "1.9396030902862549", "local_forecast": 1, "wind_burst": 4.043909664715845, "wind_direction": 86.96039494056386, "wave_height_sig": "1.4920024871826172", "date": "2016-06-29 12:00", "wave_direction": "223.59225463867188"}, {"wind_speed": 3.494804540230962, "wave_period": "17.765199661254883", "wave_height_max": "2.004603147506714", "local_forecast": 1, "wind_burst": 4.543245902300251, "wind_direction": 56.83098376732581, "wave_height_sig": "1.5420024394989014", "date": "2016-06-29 18:00", "wave_direction": "222.63827514648438"}]
        # Make sure dates in entries are all different
        date_counter = 0
        for sample in test_data:
            date = datetime.utcnow() + timedelta(hours=date_counter * 6)
            sample['date'] = date.isoformat()
            date_counter += 1
        response = self.client.post('/api/local_forecast_entry/', test_data, format='json')
        self.assertEqual(200, response.status_code)

        # Make sure the new count reflects inserted entries
        response = self.client.get('/api/local_forecast_entry/')
        self.assertEqual(200, response.status_code)
        data = response.data
        self.assertEqual(initial_count + len(test_data), data['count'])

        # Assert update works
        duplicate_data = test_data[0:5]
        response = self.client.post('/api/local_forecast_entry/', duplicate_data, format='json')
        self.assertEqual(200, response.status_code)

        # Check that the count is still the same as last time
        response = self.client.get('/api/local_forecast_entry/')
        self.assertEqual(200, response.status_code)
        data = response.data
        self.assertEqual(initial_count + len(test_data), data['count'])

    '''def test_get_week_tides(self):
        response = self.client.get('/api/tides/1/weekly_view')
        data = response.data
        self.assertEqual(len(data), 3)'''
