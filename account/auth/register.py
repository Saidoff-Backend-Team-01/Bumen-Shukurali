import json

import sentry_sdk
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

from account.models import SocialUser, User


def register_social_user(provider, user_id, email, first_name, last_name):
    try:

        filtered_user_by_email = User.objects.filter(email=email).first()
        if filtered_user_by_email:
            SocialUser.objects.update_or_create(
                user=filtered_user_by_email, auth_provider=provider, social_id=user_id
            )
            if provider == filtered_user_by_email.auth_type:
                registered_user = authenticate(
                    username=email, password=settings.SOCIAL_SECRET_PASSWORD
                )
                return json.dumps(
                    {
                        "email": registered_user.email,
                        "first_name": registered_user.first_name,
                        "last_name": registered_user.last_name,
                        "token": registered_user.get_token(),
                    }
                )
            else:
                raise AuthenticationFailed(
                    "Please continue your login using "
                    + filtered_user_by_email.auth_type
                )
        else:
            user = User.objects.create_user(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=settings.SOCIAL_SECRET_PASSWORD,
            )
            user.is_active = True
            user.auth_type = provider
            user.save()
            SocialUser.objects.update_or_create(
                user=user, auth_provider=provider, social_user_id=user_id
            )
            new_user = authenticate(
                email=email, password=settings.SOCIAL_SECRET_PASSWORD
            )
            return json.dumps(
                {
                    "email": new_user.email,
                    "first_name": new_user.first_name,
                    "last_name": new_user.last_name,
                    "token": new_user.get_token(),
                }
            )
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise AuthenticationFailed(e)
