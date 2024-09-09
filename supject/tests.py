from unicodedata import category

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from account.models import User, Groups
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from account.models import User
from supject.models import Category, Subject
from supject.serializers import CategorySerializer, SubjectSerializer

from .models import Category, SubjectTitle, UserSubject, Subject



class TestSubject(APITestCase):
    def test_category_list(self):
        categories = Category.objects.bulk_create(
            [
                Category(name="Cat 1", click_count=0),
                Category(name="Cat 2", click_count=0),
                Category(name="Cat 3", click_count=0),
            ]
        )

        url = reverse("categories")

        res = self.client.get(url)

        ser = CategorySerializer(Category.objects.all(), many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, ser.data)

    def test_category_detail(self):
        categories = Category.objects.bulk_create(
            [
                Category(name="Cat 1", click_count=0),
                Category(name="Cat 2", click_count=0),
                Category(name="Cat 3", click_count=0),
            ]
        )

        cat_1 = Category.objects.get(name="Cat 1")
        url = reverse("category-subject", kwargs={"pk": cat_1.pk})
        res = self.client.get(url)

        ser = CategorySerializer(cat_1)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # self.assertEqual(res.data[0], ser.data)

        cat_2 = Category.objects.get(name="Cat 2")
        url = reverse("category-subject", kwargs={"pk": cat_2.pk})
        res = self.client.get(url)

        ser = CategorySerializer(cat_2)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # self.assertEqual(res.data[1], ser.data)

        cat_3 = Category.objects.get(name="Cat 3")
        url = reverse("category-subject", kwargs={"pk": cat_3.pk})
        res = self.client.get(url)

        ser = CategorySerializer(cat_3)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # self.assertEqual(res.data[2], ser.data)
        #


# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase

# from .models import Category, Subject, SubjectTitle


# class CategoryListViewTests(APITestCase):

#     def setUp(self):
#         # Create test data
#         self.category = Category.objects.create(name="Test Category", click_count=10)
#         self.subject_title = SubjectTitle.objects.create(
#             name="Test Subject Title", category=self.category
#         )
#         self.subject = Subject.objects.create(
#             name="Test Subject",
#             type=Subject.SubjectType.LOCAL,
#             subject_title=self.subject_title,
#         )

#     def test_get_categories(self):
#         url = reverse("categories")
#         response = self.client.get(url, format="json")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#         self.assertEqual(response.data[0]["name"], "Test Category")
#         self.assertEqual(response.data[0]["click_count"], 10)
#         # self.assertEqual(response.data[0]['subject_titles'][0]['name'], 'Test Subject Title')
#         # self.assertEqual(len(response.data[0]['subject_titles'][0]['subjects']), 1)
#         # self.assertEqual(response.data[0]['subject_titles'][0]['subjects'][0]['name'], 'Test Subject')
#         # self.assertEqual(response.data[0]['subject_titles'][0]['subjects'][0]['type'], 'local')


class TestUserPopularSubject(APITestCase):
    def setUp(self):
        self.url = reverse("user-popular-subjects")
        category = Category.objects.create(name="Category 1")
        subject_title = SubjectTitle.objects.create(
            name="Subject Title 1", category=category
        )
        subject_title2 = SubjectTitle.objects.create(
            name="Subject Title 2", category=category
        )

        self.subject1 = Subject.objects.create(
            name="Subject 1", type="local", subject_title=subject_title
        )
        self.subject2 = Subject.objects.create(
            name="Subject 2", type="global", subject_title=subject_title
        )
        self.subject3 = Subject.objects.create(
            name="Subject 3", type="global", subject_title=subject_title2
        )

        self.user = User.objects.create_user(
            email="user@example.com", password="password"
        )
        self.new_user2 = User.objects.create_user(
            email="user2@example.com", password="password2"
        )

        UserSubject.objects.create(user=self.user, subject=self.subject1, started=True)
        UserSubject.objects.create(
            user=self.new_user2, subject=self.subject1, started=True
        )

        UserSubject.objects.create(user=self.user, subject=self.subject2, started=True)

    def test_happy(self):
        response = self.client.get(self.url)
        print(f"URL: {self.url}")
        print(f"Response Status Code: {response.status_code}")

        if response.status_code == 404:
            print(f"Response Content: {response.content.decode('utf-8')}")
        print("resp: ", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = [
            {
                "id": 1,
                "name": "Subject 1",
                "type": "local",
                "subject_title": 1,
                "steps": [],
            },
            {
                "id": 2,
                "name": "Subject 2",
                "type": "global",
                "subject_title": 1,
                "steps": [],
            },
        ]
        #
        # self.assertEqual(response.data, expected_data)
        #


# class TestSubjectView(APITestCase):
#     def setUp(self):
#         self.category1 = Category.objects.create(name="Category1", click_count=1)
#         self.user1 = User.objects.create_user(
#             email="user@example.com", password="password"
#         )

#         self.category2 = Category.objects.create(name="Category2", click_count=2)
#         self.user2 = User.objects.create_user(
#             email="user@example2.com", password="password"
#         )

# #         SubjectTitle.objects.create(name=self.user1, category=self.category1)
# #         SubjectTitle.objects.create(name=self.user2, category=self.category2)

#     def test_happy(self):
#         url = reverse("subject-search")
#         test_query = "Category1"
#         response = self.client.get(f"{url}?query={test_query}", format="json")
#         count = SubjectTitle.objects.count()
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(count, 2)

#         self.assertEqual(response.data, expected_data)




class JoinDiscussionGroupViewTests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.subject_title = SubjectTitle.objects.create(
            name="Test Title",
            category=self.category
        )
        self.user = User.objects.create(username="testuser", password="testpassword")
        self.subject = Subject.objects.create(
            name="Test Subject",
            subject_title=self.subject_title,
            type='global'  
        )
        self.user_subject = UserSubject.objects.create(user=self.user, subject=self.subject, finished=True)
        self.discussion_group = Groups.objects.create(name="Main Discussion Group")
    
    def test_join_group_success(self):
        url = reverse('join_group', args=[self.user.id, self.subject.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.discussion_group.users.filter(id=self.user.id).exists())

    def test_join_group_not_finished(self):
        self.user_subject.finished = False
        self.user_subject.save()
        url = reverse('join_group', args=[self.user.id, self.subject.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_join_group_no_group(self):
        self.discussion_group.delete()
        url = reverse('join_group', args=[self.user.id, self.subject.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

