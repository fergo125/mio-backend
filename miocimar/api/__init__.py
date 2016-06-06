from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APITestCase


class APIClientTestCase(APITestCase):
    fixtures = ["tides.json"]

    def setUp(self):
        self.client = APIClient()
