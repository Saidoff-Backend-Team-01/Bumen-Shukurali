from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from math import ceil

from .models import News
from .serializers import NewsListSerializer

class NewsListView(ListAPIView):
    queryset = News.published.all()
    serializer_class = NewsListSerializer

    def get_queryset(self):
        return self.queryset.order_by("-created_at")


class NewsListPaginationView(APIView):
    items_per_page = 9
    next_page = items_per_page + 1

    def get(self, request, page=1):
        page = int(page)
        if page <1:
            page = 1

        total_items = News.published.count()
        total_pages = ceil(total_items / self.items_per_page)
        offset = (page - 1) * self.items_per_page
        queryset = News.published.all().order_by("-created_at")[offset:offset + self.items_per_page]
        serializer = NewsListSerializer(queryset, many=True)

        return Response({
            'page': page,
            'total_pages': total_pages,
            'results': serializer.data,
            'items_on_page': len(serializer.data),
            'total_items': total_items,
        })