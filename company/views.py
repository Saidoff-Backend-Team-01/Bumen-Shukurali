from rest_framework.generics import ListAPIView, ListCreateAPIView
from company.models import Contacts, ContactUS, PrivacyPolicy, AppInfo, AboutMistake, Sponsor, SocialMedia
from company.serializers import ContactsSerializer, ContactUSSerializer, PrivacyPolicySerializer, AppInfoSerializer, SponsorSerializer, SocialMediaSerializer
# Create your views here.


class ContactsList(ListAPIView):
    queryset = Contacts.objects.all()
    serializer_class = ContactsSerializer


class ContactUSCreateList(ListCreateAPIView):
    queryset = ContactUS.objects.all()
    serializer_class = ContactUSSerializer


class PrivacyPolicyRead(ListAPIView):
    queryset = PrivacyPolicy.objects.all()
    serializer_class = PrivacyPolicySerializer



class AppInfoList(ListAPIView):
    queryset = AppInfo.objects.all()
    serializer_class = AppInfoSerializer


class SponsorsList(ListAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer


class SocialMediaRead(ListAPIView):
    queryset = SocialMedia.objects.all()
    serializer_class = SocialMediaSerializer