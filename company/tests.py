from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from .models import Contacts

# class TestContactWithUsView(APITestCase):

#     def setUp(self):
#         pass

#     def test_happy(self):
#         url = reverse("contact_with_us")
#         data = {
#             "name": "TestName",
#             "phone_number": "+998919209292",
#             "message": "TestMesssage",
#         }
#         response = self.client.post(url, data, format="json")
#         self.assertEquals(response.status_code, 201)
#         self.assertEquals(response.data["name"], "TestName")
#         self.assertEquals(
#             list(response.data.keys()), ["name", "phone_number", "message"]
#         )


class ContactsDetailViewTest(APITestCase):

    def setUp(self):
        self.contact = Contacts.objects.create(
            address="Uzbekistan Tashkent",
            phone_number="998908615795",
            email="ulugbek.husain@gmail.com",
            location="https://www.example.com"
        )

    def test_get_contact(self):
        url = reverse('contact-detail')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data['address'], self.contact.address)
        self.assertEqual(response.data['phone_number'], self.contact.phone_number)
        self.assertEqual(response.data['email'], self.contact.email)
        self.assertEqual(response.data['location'], self.contact.location)