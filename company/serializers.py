from rest_framework import serializers
from company.models import ContactUS
from common.serializers import MediaSerializer

class ContactsSerializer(serializers.Serializer):
    adress = serializers.CharField(max_length=250)
    phone = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()

class ContactUSSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    phone = serializers.CharField()
    msg = serializers.CharField()


    def create(self, validated_data):
        return ContactUS.objects.create(**validated_data)
    

class PrivacyPolicySerializer(serializers.Serializer):
    text = serializers.CharField()


class AppInfoSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()


class SponsorSerializer(serializers.Serializer):
    image = MediaSerializer()
    url = serializers.URLField()


class SocialMediaSerializer(serializers.Serializer):
    telegram = serializers.URLField()
    likedin = serializers.URLField()
    facebook = serializers.URLField()
    instagram = serializers.URLField()