from rest_framework import serializers

from common.serializers import MediaURlSerializer

from .models import FAQ, Contacts, ContactWithUs


class ContactWithUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactWithUs
        fields = ("name", "phone_number", "message")

    def create(self, validated_data):
        return ContactWithUs.objects.create(**validated_data)


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ("question", "answer")


class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = "__all__"


class AdvertisingSerializer(serializers.Serializer):
    image = MediaURlSerializer()
    url = serializers.URLField()
    created_at = serializers.DateTimeField()


class SocialMediaSerializer(serializers.Serializer):
    telegram = serializers.URLField()
    likedin = serializers.URLField()
    facebook = serializers.URLField()
    instagram = serializers.URLField()
