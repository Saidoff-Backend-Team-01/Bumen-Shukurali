from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from yaml import serialize
from company.models import FAQ, ContactWithUs,Contacts, PrivacyPolicy
from company.serializers import ContactWithUsSerializer, FAQSerializer,ContactsSerializer, PrivacyPolicySerializer
from django.utils.translation import gettext_lazy as _

from company.models import FAQ, Advertising, Contacts, ContactWithUs, SocialMedia, ContactWithUsCategory, ContactWithUsReason, ContactWithUsMobile, AppInfo, Sponsor
from company.serializers import (
    AdvertisingSerializer,
    ContactsSerializer,
    ContactWithUsSerializer,
    FAQSerializer,
    SocialMediaSerializer,
    ContactWithUsCategorySerializer,
    ContactWithUsReasonSerializer,
    ContactWithUsMobileSerializer,
    AppInfoSerializer,
    SponsorSerializer
)
# from .serializers import ContactsSerializer


class ContactWithUsView(CreateAPIView):
    queryset = ContactWithUs.objects.all()
    serializer_class = ContactWithUsSerializer


class FAQAPIView(APIView):
    serializer_class = FAQSerializer
    
    def get(self, request, *args, **kwargs):
        queryset = FAQ.objects.all()
        serializer = FAQSerializer(queryset, many=True)
        return Response(serializer.data)



class PrivacyPolicyView(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = PrivacyPolicy.objects.first()
        if queryset:
            serializer = PrivacyPolicySerializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:
            return Response({"detail": "PrivacyPolicy not found"}, status=404)



class ContactsDetailView(APIView):
    def get(self, request):
        try:
            contact = Contacts.objects.first()
            serializer = ContactsSerializer(contact)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Contacts.DoesNotExist:
            return Response(
                {"detail": _("Contact not found.")}, status=status.HTTP_404_NOT_FOUND
            )



class AdvertisingListView(ListAPIView):
    queryset = Advertising.objects.all()
    serializer_class = AdvertisingSerializer



class SocialMediaRead(ListAPIView):
    queryset = SocialMedia.objects.all()
    serializer_class = SocialMediaSerializer



class ContactWithUsCategoryAPIView(APIView):
    def get(self, request):
        categories = ContactWithUsCategory.objects.all()
        serializer = ContactWithUsCategorySerializer(categories, many=True)
        return Response(serializer.data)
    


class ContactWithUsReasonAPIView(APIView):
    def get(self, request):
        category_id = request.query_params.get('category_id')
        if category_id:
            reasons = ContactWithUsReason.objects.filter(category_id=category_id)
        else:
            reasons = ContactWithUsReason.objects.all()
        serializer = ContactWithUsReasonSerializer(reasons, many=True)
        return Response(serializer.data)
    


class ContactWithUsMobileAPIView(CreateAPIView):
    queryset = ContactWithUsMobile.objects.all()
    serializer_class = ContactWithUsMobileSerializer
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        errors = serializer.errors
        if 'file' not in request.data:
            errors['file'] = ["Fayl yuklanmadi!"]
        
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
               
            
            
class AppInfoView(APIView):
    serializer_class = AppInfoSerializer
    def get(self, request, *args, **kwargs):
        queryset = AppInfo.objects.all()
        serializer = AppInfoSerializer(queryset, many=True)
        return Response(serializer.data)



class SponsorsView(APIView):
    serializer_class = SponsorSerializer

    def get(self, request, *args, **kwargs):
        queryset = Sponsor.objects.all()
        serializer = SponsorSerializer(queryset, many=True)
        return Response(serializer.data)
