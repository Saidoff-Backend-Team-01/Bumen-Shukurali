from rest_framework import serializers
from common.models import Media, FAQ, Advertising


class MediaSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=50, required=False)
    file = serializers.FileField()


class FAQSerializer(serializers.Serializer):
    question = serializers.CharField()
    answer = serializers.CharField()


class AdvertisingSerializer(serializers.Serializer):
    image = MediaSerializer()
    url = serializers.URLField()
    created_at = serializers.DateTimeField()

    