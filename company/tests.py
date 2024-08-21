from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase


class TestContactWithUsView(APITestCase):

    def setUp(self):
        pass

    def test_happy(self):
        url = reverse("contact_with_us")
        data = {
            "name": "TestName",
            "phone_number": "+998919209292",
            "message": "TestMesssage",
        }
        response = self.client.post(url, data, format="json")
        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.data["name"], "TestName")
        self.assertEquals(
            list(response.data.keys()), ["name", "phone_number", "message"]
        )
