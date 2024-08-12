from subject.serializers import *
from subject.models import *
from rest_framework.generics import ListAPIView, RetrieveAPIView
# Create your views here.


class ClubList(ListAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer


class ClubDetail(RetrieveAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubDatailSerializer
