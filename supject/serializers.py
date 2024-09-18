from rest_framework import serializers

from account.serializers import UserSerializer
from common.serializers import MediaURlSerializer
from supject.models import (
    Category,
    Club,
    ClubMeeting,
    Step,
    StepFile,
    Subject,
    SubjectTitle,
    TestAnswer,
    TestQuestion,
    UserSubject,
    UserTestResult,
    UserTotalTestResult,
    Vacancy,
)


class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step

        fields = [
            "id",
        ]


class SubjectSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True, read_only=True)

    class Meta:
        model = Subject
        fields = ["id", "name", "type", "subject_title", "steps"]


class SubjectDetailSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True)

    class Meta:
        model = Subject
        fields = ("id", "name", "type", "steps")


class UserSubjectSerializer(serializers.ModelSerializer):
    subject = SubjectDetailSerializer()

    class Meta:
        model = UserSubject
        fields = ["id", "subject", "total_test_ball", "started_time", "started"]

class UserSubjectStartSerializer(serializers.ModelSerializer):
    subject = SubjectDetailSerializer()

    class Meta:
        model = UserSubject
        fields = ["id", "subject", "total_test_ball", "started_time", "started"]


class SubjectTitleSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True, read_only=True)

    class Meta:
        model = SubjectTitle
        fields = ["id", "name", "category", "subjects"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "click_count",]


class SubjectTitleListSerializer(serializers.ModelSerializer):
    subjects = SubjectDetailSerializer(many=True)

    class Meta:
        model = SubjectTitle
        fields = ("id", "name", "subjects")


class StepFilesSerializer(serializers.ModelSerializer):
    file = MediaURlSerializer()

    class Meta:
        model = StepFile
        fields = ["id", "title", "file"]


class StepDetailSerializer(serializers.ModelSerializer):
    step_files = StepFilesSerializer(many=True)

    class Meta:
        model = Step
        fields = ["title", "description", "step_files"]


class StartStepTestSerializer(serializers.Serializer):
    step_id = serializers.IntegerField(required=True)


class TestAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestAnswer
        fields = ("id", "answer")


class StepTestQuestionTestSerializer(serializers.ModelSerializer):
    test_answers = TestAnswerSerializer(many=True)

    class Meta:
        model = TestQuestion
        fields = ("id", "question_type", "question", "test_answers")


class UserPopularSubjectSerializer(serializers.ModelSerializer):
    start_count = serializers.IntegerField()

    class Meta:
        model = Subject
        fields = ('id', 'name', 'type', 'subject_title', 'start_count')
        
        
class SubjectSearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubjectTitle
        fields = ('id', 'name', 'category')
        
        
class CategorySearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'click_count')

class ClubSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Club
        fields = ("id", "name", "users", "subject", "description")


class ClubMeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubMeeting
        fields = "__all__"


class FinishTestQuestionSerializer(serializers.Serializer):
    question_id = serializers.IntegerField(required=True)
    answer_ids = serializers.ListField(source=serializers.IntegerField())


class StepTestFinishSerializer(serializers.Serializer):
    result_id = serializers.IntegerField(required=True)
    questions = serializers.ListField(source=FinishTestQuestionSerializer())


class UserTestResultSerializer(serializers.ModelSerializer):
    test_question = serializers.StringRelatedField()
    test_answers = TestAnswerSerializer(many=True)

    class Meta:
        model = UserTestResult
        fields = ['id', 'test_question', 'test_answers']


class UserTotalTestResultSerializer(serializers.ModelSerializer):
    user_test_results = UserTestResultSerializer(many=True)

    class Meta:
        model = UserTotalTestResult
        fields = ['id', 'step_test', 'user', 'ball', 'correct_answers', 'user_test_results', 'finished', 'percentage']
        read_only_fields = ['id', 'user', 'step_test']


class UserTestsResultIDSerializer(serializers.Serializer):
    result_id = serializers.IntegerField(required=True)


class VacancySerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    
    class Meta:
        model = Vacancy
        fields = ('name', 'category', 'description')


class JoinGroupSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    subject_id = serializers.IntegerField()
