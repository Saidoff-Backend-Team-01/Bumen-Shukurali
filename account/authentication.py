from django.contrib.auth.backends import BaseBackend

from .models import User


class PhoneEmailAuthBackend(BaseBackend):
    """
    Custom authentication backend.

    Allows users to log in using their email address or phone number.
    """

    def authenticate(self, request=None, email=None, phone=None, password=None):
        try:
            if email is not None:
                user = User.objects.get(email=email)
            else:
                user = User.objects.get(phone=phone)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
