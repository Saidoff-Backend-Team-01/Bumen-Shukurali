from rest_framework import serializers
from account.serializers import UserSerializer


class CategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    click_count = serializers.IntegerField()


    def update(self, instance, validated_data):
        instance.click_count += 1
        instance.save()

        return instance


class SubjectTitleSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    category = CategorySerializer()


class SubjectSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    type = serializers.CharField(max_length=50)
    subject_title = SubjectTitleSerializer()


class ClubSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    users = UserSerializer(many=True, read_only=True)
    description = serializers.CharField()
    subject = SubjectSerializer()


class ClubMeetingSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    location = serializers.URLField()
    date = serializers.DateTimeField()
    



class ClubDatailSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    users = UserSerializer(many=True, read_only=True)
    description = serializers.CharField()
    subject = SubjectSerializer()
    meetings = ClubMeetingSerializer(read_only=True, many=True)

