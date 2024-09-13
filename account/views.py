import hashlib
import hmac
import time
from datetime import timedelta
import uuid as uuid_lib

from django.conf import settings
from django.shortcuts import render
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.request import Request
from django.core.cache import cache
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Groups, User, UserMessage, UserOtpCode
from .permissions import IsGroupMember
from .serializers import (
    FacebookSerializer,
    GoogleSerializer,
    TelegramOauth2Serializer,
    UserMessageSerializer,
    UserOtpCodeVerifySerializer,
    UserRegisterSerializer,
)
from .utils import generate_otp_code, send_verification_code
from .tasks import send_code


class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

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
        send_verification_code(user.email, new_otp_code.code)


class UserRegisterVerifyView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserOtpCodeVerifySerializer

    def create(self, request, *args, **kwargs):
        try:

            data = self.serializer_class(data=request.data)
            if not data.is_valid():
                return Response(
                    status=status.HTTP_400_BAD_REQUEST, data={"message": "Invalid data"}
                )
            user = User.objects.get(email=data.data["email"])
            user_otp_code = UserOtpCode.objects.filter(
                user=user, code=data.data["code"], is_used=False
            )
            if not user_otp_code.exists():
                return Response(
                    status=status.HTTP_404_NOT_FOUND,
                    data={"message": "otp code not found"},
                )
            user_otp_code = user_otp_code.filter(expires_in__gte=timezone.now())
            if not user_otp_code.exists():
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"message": "otp code was expired"},
                )

            user.is_active = True
            user.save()
            otp_code = user_otp_code.first()
            otp_code.is_used = True
            otp_code.save()
            return Response(
                status=status.HTTP_200_OK, data={"message": "user is activated"}
            )
        except User.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"message": "User does not exist"},
            )


class GoogleAuth(APIView):
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
            raise PermissionDenied("You are not a member of this group.")
        serializer.save(user=self.request.user)


class MessageListApi(ListAPIView):
    serializer_class = UserMessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsGroupMember]

    def get_queryset(self):
        group_id = self.kwargs["group_id"]
        group = Groups.objects.get(pk=group_id)
        if self.request.user not in group.users.all():
            raise PermissionDenied("You are not a member of this group.")
        return UserMessage.objects.filter(group=group)


class TelegramLoginView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = TelegramOauth2Serializer

    def post(self, request, *args, **kwargs):
        auth_data = self.serializer_class(data=request.data)
        if not auth_data:
            return Response({"error": "No authentication data provided"}, status=400)

        # Step 1: Verify the data is from Telegram
        if not self.verify_telegram_authentication(auth_data):
            return Response({"error": "Invalid authentication data"}, status=400)

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


code = openapi.Parameter(
    name="code", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING
)

email = openapi.Parameter(
    name="email", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING
)

uuids = openapi.Parameter(
    name="uuids", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING
)

class ForgetPasswordCodeSend(APIView):
    @swagger_auto_schema(manual_parameters=[email])
    def post(self, request: Request):
        try:
            email = request.data.get('email', None)
            
            try:
                user = User.objects.get(email=email)
            except:
                return Response({'error': 'Not user with this email'}, status=status.HTTP_404_NOT_FOUND)
        
            send_code.delay(email=email)
            return Response({'msg': 'Code was sent to email'})
        except:
            return Response({'error': 'Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ForgetPasswordChecking(APIView):
    @swagger_auto_schema(manual_parameters=[code, email])
    def post(self, request: Request):
        try:
            code = request.data.get('code')
            email = request.data.get('email')

            user_code = cache.get(email)
            uuid = str(uuid_lib.uuid4())
            if user_code == code:
                cache.set(uuid, email, timeout=60 * 3)

                return Response({'msg': 'Enter new password', 'uuid': uuid}, status=status.HTTP_200_OK)
            
            else:
                return Response({'error': 'Code is wrong !!!'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error':'Incorrect email or code'})


class ForgetPasswordNew(APIView):
    @swagger_auto_schema(manual_parameters=[code, uuids])
    def post(self, request: Request):
        uuid = request.data.get('uuid')
        password = request.data.get('password')
        
        try:
            user = cache.get(uuid, None)

            if user:
                get_user = User.objects.get(email=user)

                get_user.set_password(password)
                get_user.save()

                cache.delete(uuid)
                
                return Response({'Msg': 'New password was saved'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'UUID is wrong !!!'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return ValueError('Incorrect email')