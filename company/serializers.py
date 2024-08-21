from rest_framework import serializers

from .models import FAQ, ContactWithUs


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
