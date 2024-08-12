from rest_framework import serializers
from news.models import News, NewsImage
from common.serializers import MediaSerializer


class NewsImageSerializer(serializers.Serializer):
    file = MediaSerializer()
    news = serializers.CharField()


class NewsViewsSerializer(serializers.Serializer):
    ip = serializers.IPAddressField()


class NewsSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    created_at = serializers.DateTimeField()
    media_id = MediaSerializer()
    images = NewsImageSerializer(many=True, source='newsImage')
    views = NewsViewsSerializer(many=True, read_only=True)
    views_count = serializers.SerializerMethodField()


    def get_views_count(self, obj):
        return obj.views.count()


