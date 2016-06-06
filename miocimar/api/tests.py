from django.test import TestCase
from . import APIClientTestCase

class APITestCase(APIClientTestCase):
    def test_get_week_tides(self):
        response = self.client.get('/api/tides/1/week')
        data = response.data
        self.assertEqual(len(data), 3)
