from rest_framework.generics import ListAPIView, RetrieveAPIView
from news.models import News
from news.serializers import NewsSerializer
from news.tasks import add_in_views

# Create your views here.
class NewsList(ListAPIView):
    queryset = News.published.all()
    serializer_class = NewsSerializer


class NewsDetail(RetrieveAPIView):
    queryset = News.published.all()
    serializer_class = NewsSerializer


    def retrieve(self, request, *args, **kwargs):
        news_id = self.get_object().pk
        ip = request.META.get('REMOTE_ADDR')

        add_in_views.delay(ip, news_id)
        return super().retrieve(request, *args, **kwargs)
