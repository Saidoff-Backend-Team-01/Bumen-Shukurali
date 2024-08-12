from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse

# Create your tests here.
class TestNewsClass(APITestCase):
    def setUp(self):
        ...
    
    def test_OK(self):
        url = reverse('newslist')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
