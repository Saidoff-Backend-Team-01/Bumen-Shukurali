from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from company.models import FAQ, ContactWithUs,Contacts
from company.serializers import ContactWithUsSerializer, FAQSerializer,ContactsSerializer

# from .serializers import ContactsSerializer

class ContactWithUsView(CreateAPIView):
    queryset = ContactWithUs.objects.all()
    serializer_class = ContactWithUsSerializer


class FAQAPIView(APIView):
    serializer_class = FAQSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            queryset = FAQ.objects.all()
            serializer = FAQSerializer(queryset, many=True)
            return Response(serializer.data)
        except Exception:
            return Response(data={"message": "Internal Server Error"}, status=500)



class ContactsDetailView(APIView):
    def get(self, request):
        try:
            contact = Contacts.objects.first()
            serializer = ContactsSerializer(contact)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Contacts.DoesNotExist:
            return Response({"detail": "Contact not found."}, status=status.HTTP_404_NOT_FOUND)
