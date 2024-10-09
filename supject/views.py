from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
)

from rest_framework import generics, permissions
from .models import Transaction, UserCard
from .serializers import TransactionSerializer, UserCardSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

import supject.serializers
from account.models import User
from common import error_codes
from supject.models import *
from supject.serializers import *
from supject.utils import calculate_test_ball

category_id = openapi.Parameter(
    name="category_id", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER
)


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class DiscountListView(ListAPIView):
    queryset = Transation.objects.all()
    serializer_class = DiscountBannerSerializer


class CategoryAPIView(APIView):
    def get(self, request, pk):
        categories = Category.objects.all().order_by("-click_count")
        # orderby clicked_count buyicha
        categories_serializer = CategorySerializer(categories, many=True)
        return Response(categories_serializer.data, status=status.HTTP_200_OK)


class SubjectListView(ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class StartSubjectApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, subject_id):
        user = request.user
        try:
            subject = Subject.objects.get(id=subject_id)
        except SubjectTitle.DoesNotExist:
            return Response(
                {"error": "Subject not found"}, status=status.HTTP_404_NOT_FOUND
            )
        # usersubject yaratamiz
        user_subject, created = UserSubject.objects.get_or_create(
            user=user, subject=subject
        )
        if created:
            user_subject.started = True
            user_subject.save()
        club = Club.objects.get(subject=subject)
        club.users.add(user)
        club.save()
        subject_serializer = UserSubjectSerializer(user_subject)
        return Response(data=subject_serializer.data, status=status.HTTP_200_OK)


class SubjectTitleApiView(ListAPIView):
    queryset = SubjectTitle.objects.all()
    serializer_class = SubjectTitleSerializer


    @swagger_auto_schema(manual_parameters=[category_id])
    def get(self, request, *args, **kwargs):
        query_param = request.query_params.get("category_id", None)
        if not query_param:
            return Response(data=[])
        subject_titles = SubjectTitle.objects.filter(category_id=query_param)
        serializer = SubjectTitleListSerializer(subject_titles, many=True)
        return Response(data=serializer.data)


class StepDetailAPIView(RetrieveAPIView):
    queryset = Step.objects.all().order_by("order")
    serializer_class = StepDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    def get(self, request, *args, **kwargs):

        try:
            step = self.get_object()
            user_subject = UserSubject.objects.filter(
                user=request.user, subject=step.subject, started=True
            )
            if user_subject.exists():
                if step.order == 1:
                    serailizer = self.serializer_class(step)
                    return Response(data=serailizer.data)
                next_step = Step.objects.get(order=step.order - 1)
                step_test = StepTest.objects.get(step=next_step)
                user_test_results = UserTotalTestResult.objects.filter(
                    step_test=step_test, user=request.user, ball__gte=60
                ).order_by("-ball")
                if user_test_results.exists():
                    serializer_new = self.serializer_class(next_step)
                    return Response(data=serializer_new.data)
                return Response(
                    data={"error": "You were not allowed to pass next step"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                return Response(
                    data={"error": "You didn't start subject yet"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Step.DoesNotExist:
            raise ValidationError("Step does not exists")
        except StepTest.DoesNotExist:
            raise ValidationError("Steptest does not exists")

        except Exception as e:
            raise APIException(e)


class StartStepTestView(CreateAPIView):
    queryset = StepTest.objects.all()
    serializer_class = StartStepTestSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            step = request.data.get("step_id")
            user_step = UserStep.objects.get(
                user=request.user, step=step, finished=False
            )
            step_test = StepTest.objects.get(step=step)
            if step_test.test_type == StepTest.TestTypes.MIDTERM:
                test_questions = TestQuestion.objects.filter(
                    Q(steptest=step_test)
                    & Q(
                        Q(level=TestQuestion.QuestionLevel.EASY)
                        | Q(level=TestQuestion.QuestionLevel.MEDIUM)
                    )
                ).order_by("?")[: step_test.question_count]
            else:
                test_questions = TestQuestion.objects.filter(
                    Q(steptest=step_test) & Q(Q(level=TestQuestion.QuestionLevel.HARD))
                ).order_by("?")[: step_test.question_count]
            user_test_result = UserTotalTestResult.objects.create(
                step_test=step_test,
                user=request.user,
            )
            user_step.finished = False
            user_step.save(update_fields=["finished"])
            data = {
                "result_id": user_test_result.id,
                "questions": StepTestQuestionTestSerializer(
                    test_questions, many=True
                ).data,
            }
            return Response(data=data)
        except Exception as e:
            raise APIException(e)


class UserClubsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, req: Request):
        user = User.objects.get(email=req.user)

        user_subjects = UserSubject.objects.filter(user=user)

        if not user_subjects.exists():
            return Response(
                {"error": "You do not have subjects so we can not enter you to club"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        clubs = []
        for i in user_subjects:
            clubs.append(ClubSerializer(Club.objects.get(subject=i.subject)).data)

        return Response({"user": UserSerializer(user).data, "clubs": clubs})


class ClubDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, req: Request, pk):
        try:
            club = Club.objects.get(pk=pk)
            meetings = ClubMeeting.objects.filter(club=club)

            return Response(
                {
                    "club": ClubSerializer(club).data,
                    "meetings": ClubMeetingSerializer(meetings, many=True).data,
                }
            )
        except Exception as e:
            raise APIException(e)


class StepTestFinishView(CreateAPIView):
    queryset = UserTotalTestResult.objects.all()
    serializer_class = StepTestFinishSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_total_test_result = self.queryset.filter(
            id=serializer.validated_data["result_id"], user=request.user, finished=False
        )
        if not user_total_test_result.exists():
            return Response(
                data={"message": error_codes.USER_TOTAL_TEST_RESULT_MSG},
                status=status.HTTP_404_NOT_FOUND,
            )
        questions = serializer.validated_data["questions"]
        total_ball = 0
        for qst in questions:
            question_ball = 0
            question = TestQuestion.objects.get(id=qst["question_id"])
            user_test_result = UserTestResult.objects.create(
                user=request.user, test_question=question
            )
            if question.question_type == TestQuestion.QuestionType.MULTIPLE:
                answers = question.answers.filter(id__in=qst["answer_ids"])
                for ans in answers:
                    user_test_result.test_answers.add(ans)
                    if ans.is_correct == True:
                        question_ball += calculate_test_ball(
                            question.question_type,
                            user_total_test_result.step_test.ball_for_each_test,
                        )
                    else:
                        continue
            else:
                answer = question.answers.filter(id__in=qst["answer_ids"]).last()
                user_test_result.test_answers.add(answer)
                if answer.is_correct == True:
                    question_ball += calculate_test_ball(
                        question.question_type,
                        user_total_test_result.step_test.ball_for_each_test,
                    )

            total_ball += question_ball

            if not answers.exists():
                return Response(
                    data={"message": error_codes.TEST_ANSWERS_NOT_EXISTS},
                    status=status.HTTP_404_NOT_FOUND,
                )
        percentage = total_ball * 100 // len(questions)
        user_total_test_result.percentage = percentage
        user_total_test_result.ball = total_ball
        user_total_test_result.save()
        user_results = UserTestResult.objects.filter(
            user=request.user, total_result=user_total_test_result
        )

        data = {
            "total_max_ball": len(questions)
            * user_total_test_result.step_test.ball_for_each_test,
            "ball": user_total_test_result.ball,
            "percentage": user_total_test_result.percentage,
            "correct_answers_count": user_results.filter(test_answers__is_correct=True),
            "incorrect_answers_count": user_results.filter(
                test_answers__is_correct=False
            ),
            "questions": "",
        }
        return Response(data=data)


class GetTestResultsView(RetrieveAPIView):
    queryset = UserTotalTestResult.objects.all()
    serializer_class = UserTotalTestResultSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        result_id = kwargs.get('result_id')
        try:
            test_result = self.queryset.get(id=result_id, user=request.user)
            serializer = self.serializer_class(test_result)
            return Response(serializer.data)
        except UserTotalTestResult.DoesNotExist:
            return Response({"message": "No test results found"}, status=status.HTTP_404_NOT_FOUND)


class SubmitTestView(CreateAPIView):
    queryset = UserTotalTestResult.objects.all()
    serializer_class = UserTestResultSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_total_test_result = self.queryset.filter(
            id=serializer.validated_data["result_id"], user=request.user, finished=False
        ).first()

        if not user_total_test_result:
            return Response(
                data={"message": "Test natijalari topilmadi yoki allaqachon yakunlangan"},
                status=status.HTTP_404_NOT_FOUND,
            )

        questions = serializer.validated_data["questions"]
        total_ball = 0

        for qst in questions:
            question_ball = 0
            question = TestQuestion.objects.get(id=qst["question_id"])
            user_test_result = UserTestResult.objects.create(
                user=request.user, test_question=question, total_result=user_total_test_result
            )

            if question.question_type == TestQuestion.QuestionType.MULTIPLE:
                answers = question.test_answers.filter(id__in=qst["answer_ids"])
                for ans in answers:
                    user_test_result.test_answers.add(ans)
                    if ans.is_correct:
                        question_ball += user_total_test_result.step_test.ball_for_each_test
            else:
                answer = question.test_answers.filter(id__in=qst["answer_ids"]).first()
                user_test_result.test_answers.add(answer)
                if answer.is_correct:
                    question_ball += user_total_test_result.step_test.ball_for_each_test

            total_ball += question_ball

        return Response({
            "message": "Test muvaffaqiyatli yakunlandi",
            "ball": total_ball,
            "percentage": user_total_test_result.percenateg
        })


class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserCardRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserCardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserCard.objects.filter(user=self.request.user)

