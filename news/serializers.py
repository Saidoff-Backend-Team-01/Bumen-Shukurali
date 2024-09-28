from rest_framework import serializers
from common.serializers import MediaURlSerializer
from news.models import News


class NewsListSerializer(serializers.ModelSerializer):
    images = MediaURlSerializer(many=True, read_only=True)

    class Meta:
        model = News
        fields = ("id", "title", "description", "created_at", "images")