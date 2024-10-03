import json

import sentry_sdk
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

from account.models import SocialUser, User
from account.utils import download_image
from common.models import Media
from core.settings import SOCIAL_SECRET_PASSWORD


def register_social_user(provider, user_id, email, first_name, last_name, photo=None):
    try:

        filtered_user_by_email = User.objects.filter(email=email).first()
        if filtered_user_by_email:
            # SocialUser.objects.update_or_create(
            #     user=filtered_user_by_email, provider=provider, social_user_id=user_id
            # )
            if provider == filtered_user_by_email.auth_type:
                logged_user = filtered_user_by_email
                return json.dumps(
                    {
                        "email": logged_user.email,
                        "first_name": logged_user.first_name,
                        "last_name": logged_user.last_name,
                        "token": logged_user.get_tokens_for_user(),
                    }
                )
            else:
                raise AuthenticationFailed(
                    "Please continue your login using "
                    + filtered_user_by_email.auth_type
                )
        else:

            user_photo = Media.objects.create(
                type=Media.MediaType.IMAGE, file=download_image(photo, user_id=user_id)
            )

            if provider.upper() == User.AuthType.FACEBOOK:
                provider = User.AuthType.FACEBOOK

            new_user = User.objects.create(
                auth_type=provider,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=SOCIAL_SECRET_PASSWORD,
                is_active=True,
                photo=user_photo,
            )

            return json.dumps(
                {
                    "email": new_user.email,
                    "first_name": new_user.first_name,
                    "last_name": new_user.last_name,
                    "token": new_user.get_tokens_for_user(),
                }
            )
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise AuthenticationFailed(e)
