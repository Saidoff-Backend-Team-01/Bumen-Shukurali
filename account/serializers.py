import requests
import sentry_sdk
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import APIException

from account.auth import facebook, google, register
from account.models import (
    IntroQuestion,
    IntroQuestionAnswer,
    SocialUser,
    User,
    UserIntroQuestion,
    UserMessage,
    UserOtpCode,
)
from common.serializers import MediaURlSerializer

from .utils import validate_uzbek_phone_number


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password", "device_id")


class UserRegisterPhoneSerializer(serializers.ModelSerializer):
    # phone_number = serializers.CharField(required=True)
    phone_number = serializers.CharField(
        required=True, validators=[validate_uzbek_phone_number]
    )

    class Meta:
        model = User
        fields = ["password", "phone_number"]

    def validate(self, attrs):
        user = User.objects.filter(phone_number=attrs["phone_number"], is_active=True)
        if user.exists():
            raise serializers.ValidationError("User already exists")

        return attrs


class UserOtpCodeVerifySerializer(serializers.Serializer):
    code = serializers.IntegerField(required=True)
    email = serializers.EmailField(required=True)


class UserPhoneVerifySerializer(serializers.Serializer):
    code = serializers.IntegerField(required=True)
    phone_number = serializers.CharField(
        required=True, validators=[validate_uzbek_phone_number]
    )


class GoogleSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):

        token_url = "https://oauth2.googleapis.com/token"
        payload = {
            "code": auth_token,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": settings.GOOGLE_GRANT_TYPE,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = requests.post(token_url, data=payload, headers=headers)

        if response.status_code == 200:
            id_token_str = response.json()["id_token"]
            user_data = google.Google.validated(id_token_str)

        else:
            raise Exception(f"Error fetching token: {response.json()}")

        if not auth_token:
            raise APIException("Код авторизации отсутствует")
        if not user_data:
            raise APIException("Ошибка верификации токена Google")

        email = user_data.get("email")
        first_name = user_data.get("given_name", "")
        last_name = user_data.get("family_name", "")
        photo = user_data.get("picture", None)
        birthday = user_data.get("birthday", None)
        username = first_name + last_name

        try:
            return register.register_social_user(
                auth_type=User.AuthType.GOOGLE,
                email=email,
                first_name=first_name,
                last_name=last_name,
                birthday=birthday,
                username=username,
                photo=photo,
            )
        except Exception as e:
            raise serializers.ValidationError(
                f"Ошибка при регистрации пользователя: {e}"
            )


class FacebookSerializer(serializers.Serializer):
    auth_token = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    photo = MediaURlSerializer(read_only=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "photo", "birth_date")


class UserMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMessage
        fields = "__all__"


class TelegramOauth2Serializer(serializers.Serializer):
    telegram_id = serializers.IntegerField()
    username = serializers.CharField()
    phone_number = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    hash = serializers.CharField()


class UserProfileSerializer(serializers.ModelSerializer):
    photo = MediaURlSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "father_name",
            "email",
            "photo",
            "birth_date",
            "gender",
            "phone_number",
        )


class ResetPasswordStartSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)

    def validate_phone_number(self, value):
        if not User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError(
                _("User with this phone number does not exist.")
            )
        return value


class ResetPasswordVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)
    otp_code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        phone_number = attrs.get("phone_number")
        otp_code = attrs.get("otp_code")

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                _("User with this phone number does not exist.")
            )

        otp_record = UserOtpCode.objects.filter(user=user, code=otp_code, is_used=False)
        if not otp_record.exists():
            raise serializers.ValidationError(_("OTP code not found or already used."))

        if otp_record.filter(expires_in__lt=timezone.now()).exists():
            raise serializers.ValidationError(_("OTP code has expired."))

        return attrs


class SetNewPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)
    new_password = serializers.CharField(min_length=8)
    confirm_password = serializers.CharField(min_length=8)

    def validate(self, attrs):
        new_password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")

        if new_password != confirm_password:
            raise serializers.ValidationError(_("Passwords do not match."))

        return attrs

    def save(self, **kwargs):
        phone_number = self.validated_data.get("phone_number")
        new_password = self.validated_data.get("new_password")

        user = User.objects.get(phone_number=phone_number)
        user.set_password(new_password)
        user.save()

        # Mark OTP as used if necessary
        UserOtpCode.objects.filter(user=user, is_used=False).update(is_used=True)

        return user


class IntroQuestionAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = IntroQuestionAnswer
        fields = ("id", "text")


class IntroQuestionSerializer(serializers.ModelSerializer):
    answers = IntroQuestionAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = IntroQuestion
        fields = ("id", "title", "more_info", "answers")


class UserIntroQuestionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    intro_questions = IntroQuestionSerializer(read_only=True)
    answer = IntroQuestionAnswerSerializer(read_only=True)

    class Meta:
        model = UserIntroQuestion
        fields = ("id", "intro_questions", "answer", "is_marked", "user")
