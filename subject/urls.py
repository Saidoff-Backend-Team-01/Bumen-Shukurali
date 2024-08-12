from django.urls import path
from subject.views import ClubDetail, ClubList



urlpatterns = [
    path('club/', ClubList.as_view(), name='clublist'),
    path('club/<int:pk>', ClubDetail.as_view(), name='clubdetail'),
]