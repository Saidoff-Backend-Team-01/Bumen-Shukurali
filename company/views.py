from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from company.models import FAQ, Contacts, ContactWithUs
from company.serializers import (
    ContactsSerializer,
    ContactWithUsSerializer,
    FAQSerializer,
)

# from .serializers import ContactsSerializer


class ContactWithUsView(CreateAPIView):
    queryset = ContactWithUs.objects.all()
    serializer_class = ContactWithUsSerializer


class FAQAPIView(APIView):
    serializer_class = FAQSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            queryset = FAQ.objects.all()
            serializer = FAQSerializer(queryset, many=True)
            return Response(serializer.data)
        except Exception:
            return Response(data={"message": _("Internal Server Error")}, status=500)


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
