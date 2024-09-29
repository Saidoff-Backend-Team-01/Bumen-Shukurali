from rest_framework import serializers
from .models import FAQ, ContactWithUs, Contacts, PrivacyPolicy
from common.serializers import MediaURlSerializer

from .models import FAQ, Contacts, ContactWithUs, ContactWithUsCategory,ContactWithUsReason,ContactWithUsMobile, AppInfo, Sponsor


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


class AppInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppInfo
        fields = ("id","title", "description")


class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ("id","image", "url")


class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = '__all__'


class PrivacyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = ('text')


class AdvertisingSerializer(serializers.Serializer):
    image = MediaURlSerializer()
    url = serializers.URLField()
    created_at = serializers.DateTimeField()


class SocialMediaSerializer(serializers.Serializer):
    telegram = serializers.URLField()
    likedin = serializers.URLField()
    facebook = serializers.URLField()
    instagram = serializers.URLField()


class ContactWithUsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactWithUsCategory
        fields = ['id', 'name']

class ContactWithUsReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactWithUsReason
        fields = ['id', 'name']

class ContactWithUsMobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactWithUsMobile
        fields = ['email', 'message', 'file', 'reason']