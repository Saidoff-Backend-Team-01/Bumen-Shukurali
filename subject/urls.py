from django.urls import path
from subject.views import ClubDetail, ClubList, SubjectList, SubjectDetail, StepDetail, LessonDetail



urlpatterns = [
    path('club/', ClubList.as_view(), name='clublist'),
    path('club/<int:pk>/', ClubDetail.as_view(), name='clubdetail'),
    path('subject/', SubjectList.as_view(), name='subject'),
    path('subject/<int:pk>/', SubjectDetail.as_view(), name='subject'),
    path('subject/<int:subject>/<int:step>/', StepDetail.as_view(), name='step'),
    path('subject/<int:subject>/<int:step>/<int:lesson>/', LessonDetail.as_view(), name='lesson'),
]