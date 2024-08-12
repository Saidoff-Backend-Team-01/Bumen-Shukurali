from django.urls import path
from common.views import MediaList, FAQList, AdvertisingList


urlpatterns = [
    path('medialist/', MediaList.as_view(), name='medialist'),
    path('faqlist/', FAQList.as_view(), name='faqlist'),
    path('adlist/', AdvertisingList.as_view(), name='adlist'),
]