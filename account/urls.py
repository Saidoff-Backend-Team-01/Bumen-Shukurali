from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    FacebookAuth,
    GoogleAuth,
    MessageListApi,
    TelegramLoginView,
    UserMessageCreateApi,
    UserRegisterVerifyView,
    UserRegisterView,
    UserRegisterPhoneView,
    UserRegisterPhoneVerifyView
)

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("register/verify/", UserRegisterVerifyView.as_view(), name="register-verify"),
    path("register/phone_number/", UserRegisterPhoneView.as_view(), name="register-phone"),
    path("register/phone_verify/", UserRegisterPhoneVerifyView.as_view(), name="register-verify-code"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("google/", GoogleAuth.as_view(), name="googleauth"),
    path("facebook/", FacebookAuth.as_view(), name="facebookauth"),
    path("messages/", UserMessageCreateApi.as_view(), name="create_message"),
    path("messages/<int:group_id>/", MessageListApi.as_view(), name="list_messages"),
    path("telegram/oauth2/", TelegramLoginView.as_view(), name="telegram-oauth2"),
]
