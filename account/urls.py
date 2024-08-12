from django.urls import path
from account.views import UserSignup, UserVerification, UserSignin, GoogleAuth



urlpatterns = [
    path('signup/', UserSignup.as_view(), name='emailsignup'),
    path('signin/', UserSignin.as_view(), name='emailsignin'),
    path('verification/', UserVerification.as_view(), name='verification'),
    path('google/', GoogleAuth.as_view(), name='googleauth')
]