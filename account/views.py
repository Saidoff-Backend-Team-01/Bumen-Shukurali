import hashlib
import hmac
import time
from datetime import timedelta

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
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Groups, User, UserMessage, UserOtpCode
from .permissions import IsGroupMember
from .serializers import (
    FacebookSerializer,
    GoogleSerializer,
    TelegramOauth2Serializer,
    UserMessageSerializer,
    UserOtpCodeVerifySerializer,
    UserPhoneVerifySerializer,
    UserProfileSerializer,
    UserRegisterPhoneSerializer,
    UserRegisterSerializer,
)
from .utils import generate_otp_code, send_verification_code, telegram_pusher

code = openapi.Parameter(name="code", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)


query = openapi.Parameter(name="query", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)


class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save(is_active=False)
        print(user.is_active)
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
        send_verification_code(user.email, new_otp_code.code)


class UserRegisterVerifyView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserOtpCodeVerifySerializer

    def create(self, request, *args, **kwargs):
        try:

            data = self.serializer_class(data=request.data)
            if not data.is_valid():
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"message": _("Invalid data")},
                )
            user = User.objects.get(email=data.data["email"])
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


class UserRegisterPhoneView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterPhoneSerializer

    def perform_create(self, serializer):
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
        telegram_pusher(user.phone_number, new_otp_code.code, new_otp_code.expires_in)

        return Response(
            {"message": "Foydalanuvchi muvaffaqiyatli ro'yxatdan o'tdi!"},
            status=status.HTTP_201_CREATED,
        )


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


class FacebookAuth(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = FacebookSerializer


class UserMessageCreateApi(CreateAPIView):
    queryset = UserMessage.objects.all()
    serializer_class = UserMessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsGroupMember]

    def perform_create(self, serializer):
        group = serializer.validated_data["group"]
        if not group.users.filter(id=self.request.user.id).exists():
            raise PermissionDenied(_("You are not a member of this group."))
        serializer.save(user=self.request.user)


class MessageListApi(ListAPIView):
    serializer_class = UserMessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsGroupMember]

    def get_queryset(self):
        group_id = self.kwargs["group_id"]
        group = Groups.objects.get(pk=group_id)
        if self.request.user not in group.users.all():
            raise PermissionDenied(_("You are not a member of this group."))
        return UserMessage.objects.filter(group=group)


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


class UserProfileView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = None

    def get_object(self):
        return self.request.user
