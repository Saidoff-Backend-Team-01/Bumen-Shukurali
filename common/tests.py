from rest_framework.test import APITestCase
from django.urls import reverse
# Create your tests here.


class TestMediaClass(APITestCase):
    def setUp(self):
        ...
    
    def is_OK(self):
        url = reverse('medialist')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 201)


class TestFAQClass(APITestCase):
    def setUp(self):
        ...
    
    def test_OK(self):
        url = reverse('faqlist')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)


class TestADClass(APITestCase):
    def setUp(self):
        ...
    
    def test_OK(self):
        url = reverse('adlist')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)


