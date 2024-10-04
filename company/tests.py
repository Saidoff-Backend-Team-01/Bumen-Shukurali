from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase
from .serializers import AppInfoSerializer
from .models import Contacts, AppInfo, ContactWithUsCategory, ContactWithUsReason, ContactWithUsMobile
from common.models import Media




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
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], "TestName")
        self.assertEqual(
            list(response.data.keys()), ["name", "phone_number", "message"]
        )

class ContactsDetailViewTest(APITestCase):
    def setUp(self):
        self.contact = Contacts.objects.create(
            address="Uzbekistan Tashkent",
            phone_number="998908615795",
            email="ulugbek.husain@gmail.com",
            location="https://www.example.com"
        )

    def test_get_contact(self):
        url = reverse('contact')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data['address'], self.contact.address)
        self.assertEqual(response.data['phone_number'], self.contact.phone_number)
        self.assertEqual(response.data['email'], self.contact.email)
        self.assertEqual(response.data['location'], self.contact.location)


# Test uchun model yaratish funksiyalari
def create_category(name="General"):
    return ContactWithUsCategory.objects.create(name=name)

def create_reason(category, name="Other"):
    return ContactWithUsReason.objects.create(name=name, category=category)

def create_media():
    # Media obyekti yaratish jarayoni (faylni saqlashga qarab bu funksiyani to'ldiring)
    return Media.objects.create(file='test_file.txt')

def create_contact(email="test@example.com", message="Test message", reason=None, file=None):
    return ContactWithUsMobile.objects.create(email=email, message=message, reason=reason, file=file)

# Test class
class ContactWithUsTests(APITestCase):
    def test_get_categories(self):
        """Kategoriyalarni olish API testi"""
        category1 = create_category(name="Support")
        category2 = create_category(name="Feedback")
        
        url = reverse('contact_with_us_categories')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], category1.name)
        self.assertEqual(response.data[1]['name'], category2.name)

    def test_get_reasons(self):
        """Belgilangan kategoriya uchun sabablardan biri olish API testi"""
        category = create_category(name="Support")
        reason1 = create_reason(category, name="Issue")
        reason2 = create_reason(category, name="Complaint")
        
        url = reverse('contact_with_us_reasons') + f'?category_id={category.id}'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], reason1.name)
        self.assertEqual(response.data[1]['name'], reason2.name)

    def test_get_all_reasons(self):
        """Kategoriya tanlanmaganda barcha sabablardan biri olish testi"""
        category1 = create_category(name="Support")
        category2 = create_category(name="Feedback")
        create_reason(category1, name="Issue")
        create_reason(category2, name="Other")
        
        url = reverse('contact_with_us_reasons')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_contact(self):
        """Yangi kontakt yuborish testi"""
        category = create_category(name="Support")
        reason = create_reason(category, name="Issue")
        
        # Faylni yuklash uchun SimpleUploadedFile ishlatamiz
        file = SimpleUploadedFile("test_file.txt", b"Test file content.", content_type="text/plain")

        url = reverse('contact_with_us_submit')
        data = {
            "email": "test@example.com",
            "message": "Test message",
            "reason": reason.id,
            "file": file
        }
        
        response = self.client.post(url, data, format='multipart')

        # Tekshirishlar
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContactWithUsMobile.objects.count(), 1)
        contact = ContactWithUsMobile.objects.first()
        self.assertEqual(contact.email, data['email'])
        self.assertEqual(contact.message, data['message'])

    def test_invalid_contact_submission(self):
        """Kontaktni to'g'ri yubormagan holda xatolik qaytarish testi"""
        url = reverse('contact_with_us_submit')
        data = {
            "email": "not-an-email",
            "message": "",
            "reason": "",
            "file": None
        }

        response = self.client.post(url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



class AppInfoViewTests(APITestCase):
    def setUp(self):
        self.app_info1 = AppInfo.objects.create(title="App1", description="First app")
        self.app_info2 = AppInfo.objects.create(title="App2", description="Second app")

    def test_get_app_info(self):
        """AppInfo ro'yxatini olish testi"""
        url = reverse('app_info')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        app_info_queryset = AppInfo.objects.all()
        serializer = AppInfoSerializer(app_info_queryset, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_internal_server_error(self):
        """Ichki xatolik yuz berganda 500 status kodi qaytarish testi"""
        url = reverse('app_info')

        AppInfo.objects.all().delete()
        
        with self.assertRaises(Exception):
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
            self.assertEqual(response.data['message'], "Internal Server Error")


from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Sponsor, Media
from .serializers import SponsorSerializer

class SponsorsViewTests(APITestCase):
    def setUp(self):
        self.media1 = Media.objects.create(file="media1.png")
        self.media2 = Media.objects.create(file="media2.png")
        self.sponsor1 = Sponsor.objects.create(image=self.media1, url="https://t.me/ulugby")
        self.sponsor2 = Sponsor.objects.create(image=self.media2, url="https://t.me/ulugby")

    def test_get_sponsors(self):
        """Sponsorlar ro'yxatini olish testi"""
        url = reverse('sponsors')
        response = self.client.get(url)

        # Tekshirishlar
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        sponsors_queryset = Sponsor.objects.all()
        serializer = SponsorSerializer(sponsors_queryset, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_internal_server_error(self):
        """Ichki xatolik yuz berganda 500 status kodi qaytarish testi"""
        url = reverse('sponsors')


        Sponsor.objects.all().delete()

        with self.assertRaises(Exception):
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
            self.assertEqual(response.data['message'], "Internal Server Error")
