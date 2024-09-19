from django.urls import path

from .views import NewsListView, NewsListPaginationView

urlpatterns = [
    path("", NewsListView.as_view(), name="news_list"),
    path('list/<int:page>/', NewsListPaginationView.as_view(), name='news-list')
]
