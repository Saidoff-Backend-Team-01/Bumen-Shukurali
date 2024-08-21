from django.conf import settings
from django.core.exceptions import ValidationError
from google.auth.transport import requests
from google.oauth2 import id_token


class Google:
    @staticmethod
    def validate(auth_token):

        try:
            id_info = id_token.verify_oauth2_token(auth_token, requests.Request())
            if "accounts.google.com" in id_info["iss"]:
                return id_info

        except Exception as e:
            return e
