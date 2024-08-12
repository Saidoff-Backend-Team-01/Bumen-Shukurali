from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

# Create your tests here.
class TestContactClass(APITestCase):
    def setUp(self):
        ...
    
    def test_OK(self):
        url = reverse('contacts')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)


class TestContactUSClass(APITestCase):
    def setUp(self):
        ...
    
    def test_get_OK(self):
        url = reverse('contactus')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)


    def test_post_OK(self):
        url = reverse('contactus')
        data = {
            'name': 'Vali',
            'phone': '+998998053845',
            'msg': 'Hello',
        }        

        req = self.client.post(url, data, format='json')
        self.assertEqual(req.status_code, 201)


class TestPrivacyPolicyClass(APITestCase):
    def setUp(self):
        ...
    
    def test_OK(self):
        url = reverse('privacypolicy')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)


class TestAppInfoClass(APITestCase):
    def setUp(self):
        ...
    
    def test_OK(self):
        url = reverse('appinfo')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)


class TestSponsorsClass(APITestCase):
    def setUp(self):
        ...
    
    def test_OK(self):
        url = reverse('sponsors')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)


class TestSocialMediaClass(APITestCase):
    def setUp(self):
        ...
    
    def test_OK(self):
        url = reverse('socialmedia')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
