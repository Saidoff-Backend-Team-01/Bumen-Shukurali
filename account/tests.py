from datetime import timedelta
from unittest import mock

from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from account.models import Groups, User, UserMessage, UserOtpCode
from common.models import Media

from account.models import IntroQuestion, IntroQuestionAnswer, UserIntroQuestion
from account.serializers import IntroQuestionSerializer, UserIntroQuestionSerializer

# class UserMessageApiTests(APITestCase):
#     def setUp(self):
#         # Create users
#         self.user1 = User.objects.create_user(username="user1", email="user1@example.com", password="password123")
#         self.user2 = User.objects.create_user(username="user2", email="user2@example.com", password="password123")

#         self.group = Groups.objects.create(name="Test Group")
#         self.group.users.add(self.user1)

#         self.media = Media.objects.create(file="/Users/noutbukcom/Desktop/Najot/amaliyot/project asosiy/Bumen-Shukurali/static/gerb_uz.png")

#         self.client = APIClient()

#         # Authenticate user1
#         self.token = RefreshToken.for_user(self.user1).access_token
#         self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

#     def test_create_message_authenticated_user(self):
#         url = reverse('create_message')
#         data = {
#             "message": "Hello, this is a test message.",
#             "file": self.media.id,
#             "group": self.group.id,
#             "user": self.user1.id
#         }
#         response = self.client.post(url, data, format='json')
#         # print(response.content)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)


#     def test_create_message_unauthenticated_user(self):
#         self.client.credentials()
#         url = reverse('create_message')
#         data = {
#             "message": "Hello, this is a test message.",
#             "file": self.media.id,
#             "group": self.group.id
#         }
#         response = self.client.post(url, data, format='json')
#         # print(response.content)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_create_message_user_not_in_group(self):
#         self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {RefreshToken.for_user(self.user2).access_token}')
#         url = reverse('create_message')
#         data = {
#             "message": "Hello, this is a test message.",
#             "file": self.media.id,
#             "group": self.group.id,
#             "user": self.user1.id
#         }
#         response = self.client.post(url, data, format='json')
#         # print(response.content)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_list_messages_authenticated_user(self):
#         UserMessage.objects.create(user=self.user1, message="Hello, this is a test message.", file=self.media, group=self.group)
#         url = reverse('list_messages', kwargs={'group_id': self.group.id})
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)

#     def test_list_messages_unauthenticated_user(self):
#         self.client.credentials()
#         url = reverse('list_messages', kwargs={'group_id': self.group.id})
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_list_messages_user_not_in_group(self):
#         self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {RefreshToken.for_user(self.user2).access_token}')
#         url = reverse('list_messages', kwargs={'group_id': self.group.id})
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AuthTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone_number="+998901234567",
            password="testpassword",
            email="test@example.com",
        )

    def test_login_success(self):
        url = reverse("token_obtain_pair")
        data = {"phone_number": "+998901234567", "password": "testpassword"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_login_invalid_credentials(self):
        url = reverse("token_obtain_pair")
        data = {"phone_number": "+998901234567", "password": "wrongpassword"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @mock.patch("account.views.telegram_pusher")
    def test_reset_password_start(self, telegram_pusher):
        telegram_pusher.return_value = 100000
        url = reverse("reset-password-start")
        data = {"phone_number": "+998901234567"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "OTP code sent to your phone.")

    def test_reset_password_verify(self):
        otp_code = UserOtpCode.objects.create(
            user=self.user,
            code="123456",
            is_used=False,
            expires_in=timezone.now() + timedelta(minutes=5),
        )
        url = reverse("reset-password-verify")
        data = {"phone_number": "+998901234567", "otp_code": "123456"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "OTP code verified successfully.")

    def test_reset_password_set(self):
        url = reverse("reset-password-set")
        data = {
            "phone_number": "+998901234567",
            "new_password": "newpassword123",
            "confirm_password": "newpassword123",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"], "Password has been reset successfully."
        )

        user = User.objects.get(phone_number="+998901234567")
        self.assertTrue(user.check_password("newpassword123"))



class IntroQuestionsViewTest(APITestCase):
    def test_list_questions_is_it_ok(self):

        question = IntroQuestion.objects.create(title='Is it test ???', more_info='It is just test')
        answer_1 = IntroQuestionAnswer.objects.create(text='Text 1', intro_question=question)
        answer_2 = IntroQuestionAnswer.objects.create(text='Text 2', intro_question=question)
        answer_3 = IntroQuestionAnswer.objects.create(text='Text 3', intro_question=question)
        answer_4 = IntroQuestionAnswer.objects.create(text='Text 4', intro_question=question)

        ser = IntroQuestionSerializer([question], many=True, read_only=True)

        url = reverse('intro_questions')
        res = self.client.get(url)


        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, ser.data)


class AnswerIntroQuestionViewTest(APITestCase):
    def test_answer_for_question_is_it_ok(self):
        question = IntroQuestion.objects.create(title='Is it test ???', more_info='It is just test')
        answer_1 = IntroQuestionAnswer.objects.create(text='Text 1', intro_question=question)
        answer_2 = IntroQuestionAnswer.objects.create(text='Text 2', intro_question=question)
        answer_3 = IntroQuestionAnswer.objects.create(text='Text 3', intro_question=question)
        answer_4 = IntroQuestionAnswer.objects.create(text='Text 4', intro_question=question)

        user = User.objects.create_user(phone_number='998053845', password='123')


        access = str(RefreshToken.for_user(user).access_token)


        url = reverse('intro_question', kwargs={'pk': 1})
        res = self.client.post(url, {'answer_id': 1}, HTTP_AUTHORIZATION=f'Bearer {access}')

        user_answer = UserIntroQuestion.objects.create(user=user, intro_question=question, is_marked=True, answer=answer_2)

        ser = UserIntroQuestionSerializer(user_answer)

        self.assertEqual(res.data, ser.data)

        

        res = self.client.post(url, {'is_marked': 'false'}, HTTP_AUTHORIZATION=f'Bearer {access}')

        self.assertEqual(res.data, {'msg': 'OK'})
        