from rest_framework.views import APIView
from account.serializers import UserSerializer, GoogleSerializer, FacebookSerializer
from account.models import User
from rest_framework.generics import CreateAPIView
from account.tasks import send_verification_code
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from rest_framework_simplejwt.tokens import RefreshToken




class UserSignup(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


    def perform_create(self, serializer):
        user = serializer.save()

        send_verification_code.delay(user.email)

        return user
    

class UserSignin(APIView):
    def post(self, req: Request):
        email = req.data.get('email')
        password = req.data.get('password')

        if not User.objects.filter(email=email).exists():
            return Response({'error': 'User with this email was not found'}, status=status.HTTP_404_NOT_FOUND)
        
        
        else:
            user = User.objects.get(email=email)

            if user.is_active == False:
                return Response({'error': 'User is not active'}, status=status.HTTP_400_BAD_REQUEST)
            

            if user.check_password(password):
                token = RefreshToken.for_user(user=user)
                return Response({'refresh_token': str(token), 'access_token': str(token.access_token)})
            
            else:
                return Response({'error': 'Wrong password'}, status=status.HTTP_400_BAD_REQUEST)




class UserVerification(APIView):
    def post(self, req: Request):
        email = req.data.get('email')
        code = req.data.get('code')

        if not User.objects.filter(email=email).exists():
            return Response({'error': 'User with this email was not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if cache.get(email) == str(code):
            user = User.objects.get(email=email)
            user.is_active = True
            user.save()
            

            token = RefreshToken.for_user(user=user)

            return Response(
                {
                    'message': 'User pass verification succecfuly !!!',
                    'tokens': {
                        'refresh_token': str(token),
                        'access_token': str(token.access_token)
                    }          
                }, 
                status=status.HTTP_200_OK)
        
        else:
            return Response({'error': 'The code is invalid or has expired'}, status=status.HTTP_400_BAD_REQUEST)




class GoogleAuth(APIView):
    def get(self, request, *args, **kwargs):
        auth_token = str(request.query_params.get('code'))
        ser = GoogleSerializer(data={'auth_token': auth_token})
        if ser.is_valid():
            return Response(ser.data)
        return Response(ser.errors, status=400)
 

class FacebookAuth(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = FacebookSerializer
    

