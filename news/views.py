from django.shortcuts import render
from rest_framework.generics import ListAPIView

from .models import News
from .serializers import NewsListSerializer


class NewsListView(ListAPIView):
    queryset = News.published.all()
    serializer_class = NewsListSerializer

    def get_queryset(self):
        return self.queryset.order_by("-created_at")
