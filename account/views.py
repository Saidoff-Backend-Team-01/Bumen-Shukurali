import hashlib
import hmac
import time
from datetime import timedelta

import sentry_sdk
from django.conf import settings
from django.shortcuts import render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import (
    Groups,
    IntroQuestion,
    IntroQuestionAnswer,
    User,
    UserIntroQuestion,
    UserMessage,
    UserOtpCode,
)
from .permissions import IsGroupMember
from .serializers import (
    FacebookSerializer,
    GoogleSerializer,
    IntroQuestionAnswerSerializer,
    IntroQuestionSerializer,
    ResetPasswordStartSerializer,
    ResetPasswordVerifySerializer,
    SetNewPasswordSerializer,
    TelegramOauth2Serializer,
    UserIntroQuestionSerializer,
    UserMessageSerializer,
    UserOtpCodeVerifySerializer,
    UserPhoneVerifySerializer,
    UserProfileSerializer,
    UserRegisterPhoneSerializer,
    UserRegisterSerializer,
)
from .utils import generate_otp_code, send_verification_code, telegram_pusher

code = openapi.Parameter(name="code", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
auth_token = openapi.Parameter(
    name="auth_token", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING
)

query = openapi.Parameter(name="query", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)


# class UserRegisterView(CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserRegisterSerializer

#     def perform_create(self, serializer):
#         user = serializer.save(is_active=False)
#         print(user.is_active)
#         user.set_password(serializer.validated_data["password"])
#         user.save()
#         code = generate_otp_code()
#         new_otp_code = UserOtpCode.objects.create(
#             user=user,
#             code=code,
#             type=UserOtpCode.VerificationType.REGISTER,
#             expires_in=timezone.now()
#             + timedelta(minutes=settings.OTP_CODE_VERIFICATION_TIME),
#         )
#         send_verification_code(user.email, new_otp_code.code)


# class UserRegisterVerifyView(CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserOtpCodeVerifySerializer

#     def create(self, request, *args, **kwargs):
#         try:

#             data = self.serializer_class(data=request.data)
#             if not data.is_valid():
#                 return Response(
#                     status=status.HTTP_400_BAD_REQUEST,
#                     data={"message": _("Invalid data")},
#                 )
#             user = User.objects.get(email=data.data["email"])
#             user_otp_code = UserOtpCode.objects.filter(
#                 user=user, code=data.data["code"], is_used=False
#             )
#             if not user_otp_code.exists():
#                 return Response(
#                     status=status.HTTP_404_NOT_FOUND,
#                     data={"message": _("otp code not found")},
#                 )
#             user_otp_code = user_otp_code.filter(expires_in__gte=timezone.now())
#             if not user_otp_code.exists():
#                 return Response(
#                     status=status.HTTP_400_BAD_REQUEST,
#                     data={"message": _("otp code was expired")},
#                 )

#             user.is_active = True
#             user.save()
#             otp_code = user_otp_code.first()
#             otp_code.is_used = True
#             otp_code.save()
#             return Response(
#                 status=status.HTTP_200_OK, data={"message": _("user is activated")}
#             )
#         except User.DoesNotExist:
#             return Response(
#                 status=status.HTTP_404_NOT_FOUND,
#                 data={"message": _("User does not exist")},
#             )


class UserRegisterPhoneView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterPhoneSerializer
    code = generate_otp_code()

    def perform_create(self, serializer):
        try:
            phone_number = serializer.validated_data["phone_number"]
            user = User.objects.filter(phone_number=phone_number).last()
            code = generate_otp_code()

            if user and not user.is_active:
                new_otp_code = UserOtpCode.objects.create(
                    user=user,
                    code=code,
                    type=UserOtpCode.VerificationType.REGISTER,
                    expires_in=timezone.now()
                    + timedelta(minutes=settings.OTP_CODE_VERIFICATION_TIME),
                )
                telegram_pusher(
                    user.phone_number,
                    new_otp_code.code,
                    new_otp_code.expires_in,
                    "registration",
                )
            else:

                user = serializer.save(is_active=False)
                user.set_password(serializer.validated_data["password"])
                user.save()

                code = generate_otp_code()
                new_otp_code = UserOtpCode.objects.create(
                    user=user,
                    code=code,
                    type=UserOtpCode.VerificationType.REGISTER,
                    expires_in=timezone.now()
                    + timedelta(minutes=settings.OTP_CODE_VERIFICATION_TIME),
                )
                telegram_pusher(
                    user.phone_number, new_otp_code.code, new_otp_code.expires_in
                )
        except Exception as e:
            sentry_sdk.capture_message(e)


class UserRegisterPhoneVerifyView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserPhoneVerifySerializer

    def create(self, request, *args, **kwargs):
        try:
            data = self.serializer_class(data=request.data)
            if not data.is_valid():
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"message": _("Invalid data")},
                )
            user = User.objects.get(phone_number=data.data["phone_number"])
            user_otp_code = UserOtpCode.objects.filter(
                user=user, code=data.data["code"], is_used=False
            )
            if not user_otp_code.exists():
                return Response(
                    status=status.HTTP_404_NOT_FOUND,
                    data={"message": _("otp code not found")},
                )
            user_otp_code = user_otp_code.filter(expires_in__gte=timezone.now())
            if not user_otp_code.exists():
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"message": _("otp code was expired")},
                )

            user.is_active = True
            user.save()
            otp_code = user_otp_code.first()
            otp_code.is_used = True
            otp_code.save()
            return Response(
                status=status.HTTP_200_OK, data={"message": _("user is activated")}
            )
        except User.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"message": _("User does not exist")},
            )


class GoogleAuth(APIView):
    @swagger_auto_schema(manual_parameters=[code])
    def get(self, request, *args, **kwargs):
        auth_token = str(request.query_params.get("code"))
        ser = GoogleSerializer(data={"auth_token": auth_token})
        if ser.is_valid():
            return Response(ser.data)
        return Response(ser.errors, status=400)


import json

from account.auth import facebook, register


class FacebookAuth(CreateAPIView):
    serializer_class = FacebookSerializer

    def post(self, request, *args, **kwargs):
        ser = self.serializer_class(data=request.data)
        try:

            if ser.is_valid():
                user_data = facebook.Facebook.validated(
                    auth_token=ser.data["auth_token"]
                )
                email = user_data.get("email")
                first_name = user_data.get("first_name", "")
                last_name = user_data.get("last_name", "")
                photo = user_data["picture"]["data"]["url"]

                data = register.register_social_user(
                    user_id=user_data.get("id"),
                    provider=User.AuthType.FACEBOOK,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    photo=photo,
                )
                return Response(json.loads(data))
            return Response(ser.errors, status=400)
        except Exception as e:
            raise Exception(e)


class UserMessageCreateApi(CreateAPIView):
    queryset = UserMessage.objects.all()
    serializer_class = UserMessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsGroupMember]

    def perform_create(self, serializer):
        group = serializer.validated_data["group"]
        if not group.users.filter(id=self.request.user.id).exists():
            raise PermissionDenied(_("You are not a member of this group."))
        serializer.save(user=self.request.user)


# class MessageListApi(ListAPIView):
#     serializer_class = UserMessageSerializer
#     # permission_classes = [permissions.IsAuthenticated, IsGroupMember]

#     def get_queryset(self):
#         group_id = self.kwargs["group_id"]
#         group = Groups.objects.get(pk=group_id)
#         if self.request.user not in group.users.all():
#             raise PermissionDenied(_("You are not a member of this group."))
#         return UserMessage.objects.filter(group=group)

class MessageListApi(ListAPIView):
    serializer_class = UserMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        group_id = self.request.query_params.get('group_id', None)
        queryset = UserMessage.objects.all()

        if group_id:
            queryset = queryset.filter(group_id=group_id)

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        """
        Update the status of a user message if the user is an admin.
        """
        message_id = request.data.get('message_id')
        new_status = request.data.get('status')

        if not message_id or not new_status:
            return Response({"error": "message_id and status are required."}, status=status.HTTP_400_BAD_REQUEST)

        if not request.user.is_staff:
            raise PermissionDenied(_("You do not have permission to perform this action."))

        try:
            message = UserMessage.objects.get(id=message_id)
            message.status = new_status
            message.save()
            return Response({"success": _("Message status updated successfully.")}, status=status.HTTP_200_OK)
        except UserMessage.DoesNotExist:
            return Response({"error": _("Message not found.")}, status=status.HTTP_404_NOT_FOUND)


class TelegramLoginView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = TelegramOauth2Serializer

    def post(self, request, *args, **kwargs):
        auth_data = self.serializer_class(data=request.data)
        if not auth_data:
            return Response({"error": _("No authentication data provided")}, status=400)

        # Step 1: Verify the data is from Telegram
        if not self.verify_telegram_authentication(auth_data):
            return Response({"error": _("Invalid authentication data")}, status=400)

        # Step 2: Create or retrieve user
        user, created = User.objects.get_or_create(
            telegram_id=auth_data["id"],
            defaults={
                "username": auth_data["username"] or f'tg_{auth_data["id"]}',
                "first_name": auth_data["first_name"],
                "last_name": auth_data.get("last_name", ""),
                "phone_number": auth_data.get("phone_number", ""),
            },
        )

        # Step 3: Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )

    def verify_telegram_authentication(self, auth_data):
        bot_token = settings.TELEGRAM_BOT_TOKEN
        data_check_string = "\n".join(
            [f"{k}={v}" for k, v in sorted(auth_data.items()) if k != "hash"]
        )
        secret_key = hashlib.sha256(bot_token.encode()).digest()
        hash_check = hmac.new(
            secret_key, data_check_string.encode(), hashlib.sha256
        ).hexdigest()

        if auth_data["hash"] != hash_check:
            return False

        auth_date = int(auth_data["auth_date"])
        current_timestamp = int(time.time())

        # Allow a certain time window for authentication
        if current_timestamp - auth_date > 86400:  # 1 day in seconds
            return False
        return True


class ResetPasswordStartView(CreateAPIView):
    serializer_class = ResetPasswordStartSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data["phone_number"]
        user = User.objects.get(phone_number=phone_number)

        code = generate_otp_code()
        new_otp_code = UserOtpCode.objects.create(
            user=user,
            code=code,
            is_used=False,
            expires_in=timezone.now()
            + timedelta(minutes=settings.OTP_CODE_VERIFICATION_TIME),
        )
        telegram_pusher(phone_number, code, new_otp_code.expires_in, "resetpassword")

        return Response(
            {"message": _("OTP code sent to your phone.")}, status=status.HTTP_200_OK
        )


class ResetPasswordVerifyView(CreateAPIView):
    serializer_class = ResetPasswordVerifySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            {"message": _("OTP code verified successfully.")}, status=status.HTTP_200_OK
        )


class SetNewPasswordView(CreateAPIView):
    serializer_class = SetNewPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": _("Password has been reset successfully.")},
            status=status.HTTP_200_OK,
        )


class UserProfileView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = None

    def get_object(self):
        return self.request.user


class IntroQuestionsView(ListAPIView):
    queryset = IntroQuestion.objects.all().order_by("?")
    serializer_class = IntroQuestionSerializer
    permission_classes = [IsAuthenticated]


class AnswerIntroQuestionView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "answer_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID of the answer",
                    required=[],
                ),
            },
        )
    )
    def post(self, req: Request, pk: int):
        answer_id = req.data.get("answer_ids")
        try:
            intro_question = IntroQuestion.objects.get(pk=pk)

        except:
            return Response(
                {"error": "Question was not found !!!"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if answer_id is None:
            UserIntroQuestion.objects.get_or_create(
                is_marked=False, intro_question=intro_question, user=req.user
            )
            return Response({"msg": "OK"}, status=status.HTTP_201_CREATED)

        try:
            answer = IntroQuestionAnswer.objects.get(pk=int(answer_id))
        except:
            return Response(
                {"error": "Answer was not found !!!"}, status=status.HTTP_404_NOT_FOUND
            )

        user_answer, created = UserIntroQuestion.objects.get_or_create(
            user=req.user, intro_question=intro_question, is_marked=True, answer=answer
        )

        return Response(UserIntroQuestionSerializer(user_answer).data)
