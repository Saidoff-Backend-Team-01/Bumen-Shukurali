from django.urls import path
from news.views import NewsList, NewsDetail



urlpatterns = [
    path('news/', NewsList.as_view(), name='newslist'),
    path('news/<int:pk>', NewsDetail.as_view(), name='newsdetail'),
]