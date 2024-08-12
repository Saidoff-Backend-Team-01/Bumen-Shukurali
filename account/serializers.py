from rest_framework import serializers
from common.serializers import MediaSerializer
from common.models import Media
from account.models import User
from .auth.google import Google
from .auth.register import register_social_user
import requests
from rest_framework.exceptions import APIException
from django.conf import settings



class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    first_name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100, write_only=True)
    photo = MediaSerializer()
    birthday = serializers.DateTimeField() 


    def create(self, validated_data):
        password = validated_data.pop('password')
        file = validated_data.pop('photo')['file']
        photo = Media.objects.create(type='image', file=file)
        user = User.objects.create_user(photo=photo, **validated_data)
        user.set_password(password)
        user.save()

        return user
    


class GoogleSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        
        token_url = 'https://oauth2.googleapis.com/token'
        payload = {
            'code': auth_token,
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRET,
            'redirect_uri': settings.GOOGLE_REDIRECT_URI,
            'grant_type': settings.GOOGLE_GRANT_TYPE,
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.post(token_url, data=payload, headers=headers)


        if response.status_code == 200:
            id_token_str = response.json()['id_token'] 
            user_data = Google.validated(id_token_str)

        else:
            raise Exception(f'Error fetching token: {response.json()}')

        if not auth_token:
            raise APIException('Код авторизации отсутствует')
        if not user_data:
            raise APIException('Ошибка верификации токена Google')



        email = user_data.get("email")
        first_name = user_data.get("given_name", "")
        last_name = user_data.get("family_name", "")
        photo = user_data.get("picture", None)
        birthday = user_data.get("birthday", None)
        username = first_name + last_name

        try:
            return register_social_user(
                auth_type=User.AuthType.GOOGLE,
                email=email,
                first_name=first_name,
                last_name=last_name,
                birthday=birthday,
                username=username,
                photo=photo,
            )
        except Exception as e:
            raise serializers.ValidationError(f'Ошибка при регистрации пользователя: {e}')
        



