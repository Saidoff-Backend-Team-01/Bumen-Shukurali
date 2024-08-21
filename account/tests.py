from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from account.models import User, Groups, UserMessage
from common.models import Media
from rest_framework_simplejwt.tokens import RefreshToken

class UserMessageApiTests(APITestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username="user1", email="user1@example.com", password="password123")
        self.user2 = User.objects.create_user(username="user2", email="user2@example.com", password="password123")

        self.group = Groups.objects.create(name="Test Group")
        self.group.users.add(self.user1)

        self.media = Media.objects.create(file="/Users/noutbukcom/Desktop/Najot/amaliyot/project asosiy/Bumen-Shukurali/static/gerb_uz.png")

        self.client = APIClient()
        
        # Authenticate user1
        self.token = RefreshToken.for_user(self.user1).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_message_authenticated_user(self):
        url = reverse('create_message')
        data = {
            "message": "Hello, this is a test message.",
            "file": self.media.id,
            "group": self.group.id,
            "user": self.user1.id
        }
        response = self.client.post(url, data, format='json')
        # print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_create_message_unauthenticated_user(self):
        self.client.credentials()
        url = reverse('create_message')
        data = {
            "message": "Hello, this is a test message.",
            "file": self.media.id,
            "group": self.group.id
        }
        response = self.client.post(url, data, format='json')
        # print(response.content)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_message_user_not_in_group(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {RefreshToken.for_user(self.user2).access_token}')
        url = reverse('create_message')
        data = {
            "message": "Hello, this is a test message.",
            "file": self.media.id,
            "group": self.group.id,
            "user": self.user1.id
        }
        response = self.client.post(url, data, format='json')
        # print(response.content)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_messages_authenticated_user(self):
        UserMessage.objects.create(user=self.user1, message="Hello, this is a test message.", file=self.media, group=self.group)
        url = reverse('list_messages', kwargs={'group_id': self.group.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_messages_unauthenticated_user(self):
        self.client.credentials()
        url = reverse('list_messages', kwargs={'group_id': self.group.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_messages_user_not_in_group(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {RefreshToken.for_user(self.user2).access_token}')
        url = reverse('list_messages', kwargs={'group_id': self.group.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
