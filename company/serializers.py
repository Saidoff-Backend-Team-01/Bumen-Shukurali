from rest_framework import serializers
from .models import FAQ, ContactWithUs, Contacts, PrivacyPolicy

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
        fields = '__all__'


class PrivacyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = '__all__'
