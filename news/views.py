from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from math import ceil
from .models import News
from .serializers import NewsListSerializer


class PageNumberPagination(PageNumberPagination):
    page_size = 9
    
    
class NewsListView(ListAPIView):
    queryset = News.published.all()
    serializer_class = NewsListSerializer
    pagination_class = PageNumberPagination
    
    def get_queryset(self):
        return self.queryset.order_by("-created_at")