from common.serializers import MediaSerializer, FAQSerializer, AdvertisingSerializer
from common.models import Media, FAQ, Advertising
from rest_framework.generics import ListAPIView
# Create your views here.


class MediaList(ListAPIView):
    serializer_class = MediaSerializer
    

    def get_queryset(self):
        queryset = Media.objects.all()
        media_type = self.request.query_params.get('type', False)  

        if media_type:
            queryset = queryset.filter(type=media_type)

        return queryset
    

class FAQList(ListAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer


class AdvertisingList(ListAPIView):
    queryset = Advertising.objects.all()
    serializer_class = AdvertisingSerializer