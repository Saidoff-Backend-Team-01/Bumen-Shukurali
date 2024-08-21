import datetime
from unittest import mock

import pytz
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from news.models import News


class TestNewsListView(APITestCase):
    url = reverse("news_list")

    def setUp(self):
        self.news1 = News.published.create(
            title="testnews",
            description="testnews",
            created_at=timezone.now(),
        )
        self.news2 = News.published.create(
            title="testnews2",
            description="testnews2",
            created_at=timezone.now(),
        )

    def test_happy(self):
        resp = self.client.get(self.url)
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(len(resp.data), 2)

        # mocked = datetime.datetime(2018, 4, 4, 0, 0, 0, tzinfo=pytz.utc)
        # with mock.patch('django.utils.timezone.now', mock.Mock(return_value=mocked)):
        #     news1 = News.published.create(
        #         title="testnews",
        #         description="testnews",
        #     )
        #     self.assertEqual(news1.created_at, mocked.strftime("%Y-%m-%d %H:%M:%S %Z"))
        #     expected_dict1 = {
        #         "id": 1,
        #         "title": "testnews",
        #         "description": "testnews",
        #         "created_at": mocked,
        #         "image": None
        #     }
        #     self.assertDictEqual(resp.data[1], expected_dict1)
