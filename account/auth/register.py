import json
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from account.models import User
from common.models import Media
from django.conf import settings


def register_social_user(auth_type, email, first_name, last_name, birthday, username, photo):
    from account.serializers import UserSerializer

    try:
        filter_by_email = User.objects.filter(email=email).exists()

        if filter_by_email:
            user = User.objects.get(email=email)
            if user.auth_type == auth_type:
                token = RefreshToken.for_user(user=user)

                return {
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'photo': str(photo) if photo else '',
                    'birthday': str(user.birthday) if user.birthday else '',
                    'auth_type': user.auth_type,
                    'tokens': {
                        'access_token': str(token.access_token),
                        'refresh_token': str(token),
                    }
                }
            
            else:
                raise AuthenticationFailed('Please continue with' + user.auth_type)
        else:
            photo = Media.objects.create(file=photo, type='image')
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, birthday=birthday, photo=photo, auth_type=auth_type)
            user.set_password(settings.SOCIAL_USER_PASSWORD)
            user.save()
            token = RefreshToken.for_user(user=user)

            return {
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'photo': str(photo) if photo else '',
                'birthday': str(user.birthday) if user.birthday else '',
                'auth_type': user.auth_type,
                'tokens': {
                    'access_token': str(token.access_token),
                    'refresh_token': str(token),
                }

            }
            
            
    
    except Exception as e:
        raise AuthenticationFailed(e)
    