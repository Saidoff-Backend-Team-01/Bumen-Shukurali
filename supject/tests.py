from rest_framework.test import APITestCase
from supject.models import Category, Subject
from supject.serializers import CategorySerializer, SubjectSerializer
from django.urls import reverse
from rest_framework import status


class TestSubject(APITestCase):
    def test_category_list(self):
        categories = Category.objects.bulk_create([
            Category(name='Cat 1', click_count=0),
            Category(name='Cat 2', click_count=0),
            Category(name='Cat 3', click_count=0),
        ])

        url = reverse('categories')

        res = self.client.get(url)

        ser = CategorySerializer(Category.objects.all(), many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, ser.data)

    
    def test_category_detail(self):
        categories =  Category.objects.bulk_create([
            Category(name='Cat 1', click_count=0),
            Category(name='Cat 2', click_count=0),
            Category(name='Cat 3', click_count=0),
        ])


        cat_1 = Category.objects.get(name='Cat 1')
        url = reverse('category-subject', kwargs={'pk': cat_1.pk})
        res = self.client.get(url)
        
        ser = CategorySerializer(cat_1)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0], ser.data)


        cat_2 = Category.objects.get(name='Cat 2')
        url = reverse('category-subject', kwargs={'pk': cat_2.pk})
        res = self.client.get(url)

        ser = CategorySerializer(cat_2)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[1], ser.data)

        
        cat_3 = Category.objects.get(name='Cat 3')
        url = reverse('category-subject', kwargs={'pk': cat_3.pk})
        res = self.client.get(url)

        
        ser = CategorySerializer(cat_3)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[2], ser.data)
    


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


