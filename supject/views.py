from django.db.models import Count, F, Q
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import APIException, NotFound, ValidationError
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

import supject.serializers
from account.models import Groups, User
from common import error_codes
from supject.models import *
from supject.serializers import *
from supject.utils import calculate_test_ball

category_id = openapi.Parameter(
    name="category_id", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER
)

query = openapi.Parameter(name="query", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)


class CategoryListView(ListAPIView):
    queryset = Category.objects.all().order_by("-click_count")
    serializer_class = CategorySerializer


class CategoryAPIView(APIView):
    def get(self, request: Request, pk):
        try:
            category = Category.objects.filter(pk=pk).update(
                click_count=F("click_count") + 1
            )
            category = Category.objects.get(pk=pk)
            subjects = Subject.objects.filter(category=category)
            category_serializer = SubjectSerializer(subjects, many=True)
            return Response(category_serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": _(f"Category was not found {e}")},
                status=status.HTTP_404_NOT_FOUND,
            )


class SubjectListView(ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class StartSubjectApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, subject_id):
        user = request.user
        try:
            subject = Subject.objects.get(id=subject_id)
        except Subject.DoesNotExist:
            return Response(
                {"error": _("Subject not found")}, status=status.HTTP_404_NOT_FOUND
            )
        # usersubject yaratamiz
        user_subject, created = UserSubject.objects.get_or_create(
            user=user, subject=subject
        )
        if created:
            user_subject.started = True
            user_subject.save()

        club, created_club = Club.objects.get_or_create(subject=subject)
        club.users.add(user)
        club.save()
        subject_serializer = UserSubjectSerializer(user_subject)
        return Response(data=subject_serializer.data, status=status.HTTP_200_OK)


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
                    data={"error": _("You were not allowed to pass next step")},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                return Response(
                    data={"error": _("You didn't start subject yet")},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Step.DoesNotExist:
            raise ValidationError(_("Step does not exists"))

        except StepTest.DoesNotExist:
            raise ValidationError(_("Steptest does not exists"))

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


class UserPopularSubject(APIView):
    def get(self, request):
        started_subjects = (
            UserSubject.objects.filter(started=True)
            .values("subject")
            .annotate(start_count=Count("subject_id"))
            .order_by("-start_count")
        )

        if not started_subjects:
            return Response({"error": _("No subjects found")}, status=404)

        subject_ids = [item["subject"] for item in started_subjects]
        subjects = Subject.objects.filter(id__in=subject_ids)

        serializer = SubjectSerializer(subjects, many=True)

        for subject in serializer.data:
            subject_id = subject["id"]
            subject["start_count"] = next(
                item["start_count"]
                for item in started_subjects
                if item["subject"] == subject_id
            )

        return Response(serializer.data)


class SubjectSearchApiView(ListAPIView):
    queryset = Category.objects.all()

    @swagger_auto_schema(manual_parameters=[query])
    def get(self, request, *args, **kwargs):
        query_param = request.query_params.get("query", None)
        if not query_param:
            return Response(data=[])

        subject_categories = Category.objects.filter(name__icontains=query_param)
        subject_categories_serializer = CategorySearchSerializer(
            subject_categories, many=True
        )
        return Response(data=subject_categories_serializer.data)


class UserClubsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, req: Request):

        user_subjects = UserSubject.objects.filter(user=req.user)

        if not user_subjects.exists():
            return Response(
                {
                    "error": _(
                        "You do not have subjects so we can not enter you to club"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        clubs = []
        for i in user_subjects:
            clubs.append(ClubSerializer(Club.objects.get(subject=i.subject)).data)

        return Response({"user": UserSerializer(req.user).data, "clubs": clubs})


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
        ).last()
        if not user_total_test_result:
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
                user=request.user,
                test_question=question,
                total_result=user_total_test_result,
            )

            # Tartiblanadigan savollar
            if question.question_type == TestQuestion.QuestionType.ORDERING:
                correct_answers = list(question.test_answers.order_by('order').values_list('id', flat=True))

                user_answers = qst["answer_ids"]
                correct_count = 0

                # if correct_answers == user_answers:
                #     question_ball += user_total_test_result.step_test.ball_for_each_test
                # else:
                #     continue

                for idx, user_answer in enumerate(user_answers):
                    if idx < len(correct_answers) and user_answer == correct_answers[idx]:
                        correct_count += 1
                    else:
                        continue

                total_answers = len(correct_answers)
                correct_percentage = correct_count / total_answers

                question_ball += correct_percentage * user_total_test_result.step_test.ball_for_each_test

            if question.question_type == TestQuestion.QuestionType.MULTIPLE:
                answers = question.test_answers.filter(id__in=qst["answer_ids"])
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
                answer = question.test_answers.filter(id__in=qst["answer_ids"]).last()
                user_test_result.test_answers.add(answer)
                if answer.is_correct == True:
                    question_ball += calculate_test_ball(
                        question.question_type,
                        user_total_test_result.step_test.ball_for_each_test,
                    )

            total_ball += question_ball

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
            "correct_answers_count": user_results.filter(
                test_answers__is_correct=True
            ).count(),
            "incorrect_answers_count": user_results.filter(
                test_answers__is_correct=False
            ).count(),
            "questions": UserTestResultSerializer(
                user_total_test_result.total_results.all(), many=True
            ).data,
        }
        return Response(data=data)


class GetTestResultsView(RetrieveAPIView):
    queryset = UserTotalTestResult.objects.all()
    serializer_class = UserTotalTestResultSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        result_id = kwargs.get("result_id")
        try:
            test_result = self.queryset.get(id=result_id, user=request.user)
            serializer = self.serializer_class(test_result)
            return Response(serializer.data)
        except UserTotalTestResult.DoesNotExist:
            raise NotFound(_("Test result not found"))


class UserSubjectListApiView(ListAPIView):
    serializer_class = UserSubjectStartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return UserSubject.objects.filter(user=user, started=True)


class UserPopularSubject(APIView):
    def get(self, request):
        started_subjects = (
            UserSubject.objects.filter(started=True)
            .values("subject")
            .annotate(start_count=Count("subject_id"))
            .order_by("-start_count")
        )

        if not started_subjects:
            return Response({"error": "No subjects found"}, status=404)

        subject_ids = [item["subject"] for item in started_subjects]
        subjects = Subject.objects.filter(id__in=subject_ids)

        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)


class JoinDiscussionGroupView(APIView):
    def post(self, request, user_id, subject_id):
        user_subject = get_object_or_404(
            UserSubject, user_id=user_id, subject_id=subject_id
        )

        if not user_subject.finished:
            return Response(
                {"detail": "The user has not yet completed the course."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        discussion_group = Groups.objects.first()
        if discussion_group:
            discussion_group.add_member(user_subject.user)
            return Response(
                {"detail": "The user joined the feedback group."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"detail": "No feedback team was found."},
                status=status.HTTP_404_NOT_FOUND,
            )


class TopUserList(APIView):
    def get(self, req: Request):
        users = User.objects.all()

        sorted_users = sorted(users, key=lambda user: user.user_total_bal, reverse=True)

        return Response(UserSerializer(sorted_users, many=True))


class SubmitTestView(CreateAPIView):
    queryset = UserTotalTestResult.objects.all()
    serializer_class = UserTestResultForSubmitSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_total_test_result = self.queryset.filter(
            id=serializer.validated_data["result_id"], user=request.user, finished=False
        ).first()

        if not user_total_test_result:
            return Response(
                data={
                    "message": "Test natijalari topilmadi yoki allaqachon yakunlangan"
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        questions = serializer.validated_data["test_question"]
        total_ball = 0

        for qst in questions:
            question_ball = 0
            question = TestQuestion.objects.get(id=qst["question_id"])
            user_test_result = UserTestResult.objects.create(
                user=request.user,
                test_question=question,
                total_result=user_total_test_result,
            )

            if question.question_type == TestQuestion.QuestionType.MULTIPLE:
                answers = question.test_answers.filter(id__in=qst["answer_ids"])
                for ans in answers:
                    user_test_result.test_answers.add(ans)
                    if ans.is_correct:
                        question_ball += (
                            user_total_test_result.step_test.ball_for_each_test
                        )
            elif question.question_type == TestQuestion.QuestionType.ORDERING:
                answers_order_list = []
                for answer_id in qst["answer_ids"]:
                    answers_order_list.append(
                        question.test_answers.get(id=answer_id).order
                    )

                if answers_order_list == qst["answer_ids"]:
                    question_ball += user_total_test_result.step_test.ball_for_each_test
                else:
                    continue

            else:
                answer = question.test_answers.filter(id__in=qst["answer_ids"]).first()
                user_test_result.test_answers.add(answer)
                if answer.is_correct:
                    question_ball += user_total_test_result.step_test.ball_for_each_test

            total_ball += question_ball

        user_total_test_result.ball = total_ball
        user_total_test_result.percentage = (
            total_ball
            / (len(questions) * user_total_test_result.step_test.ball_for_each_test)
        ) * 100
        user_total_test_result.finished = True
        user_total_test_result.save()

        return Response(
            {
                "message": "Test muvaffaqiyatli yakunlandi",
                "ball": total_ball,
                "percentage": user_total_test_result.percentage,
            }
        )
