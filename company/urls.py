from django.urls import path
from company.views import ContactsList, ContactUSCreateList, PrivacyPolicyRead, AppInfoList, SponsorsList, SocialMediaRead


urlpatterns = [
    path('contacts/', ContactsList.as_view(), name='contacts'),
    path('contactus/', ContactUSCreateList.as_view(), name='contactus'),
    path('privacypolicy/', PrivacyPolicyRead.as_view(), name='privacypolicy'),
    path('appinfo/', AppInfoList.as_view(), name='appinfo'),
    path('sponsors/', SponsorsList.as_view(), name='sponsors'),
    path('socialmedia/', SocialMediaRead.as_view(), name='socialmedia'),
]