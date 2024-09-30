from rest_framework import serializers
from common.serializers import MediaURlSerializer
from news.models import News, NewsImage


# class NewsListSerializer(serializers.ModelSerializer):
#     images = MediaURlSerializer(many=True, read_only=True)

#     class Meta:
#         model = News
#         fields = ("id", "title", "description", "created_at", "images")


class NewsImageSerializer(serializers.ModelSerializer):
    image = MediaURlSerializer(read_only=True)

    class Meta:
        model = NewsImage
        fields = ('id', 'image')

class NewsDetailSerializer(serializers.ModelSerializer):
    news_images = NewsImageSerializer(many=True, read_only=True)

    class Meta:
        model = News
        fields = ("id", "title", "description", "created_at", "news_images")