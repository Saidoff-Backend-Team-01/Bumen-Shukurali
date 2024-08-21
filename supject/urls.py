from django.urls import path

from .views import (
    CategoryAPIView,
    CategoryListView,
    ClubDetail,
    UserClubsView,
    StartStepTestView,
    StartSubjectApi,
    StepDetailAPIView,
    SubjectTitleApiView,
    GetTestResultsView,
)

urlpatterns = [
    path("category/<int:pk>/", CategoryAPIView.as_view(), name="category-subject"),
    path(
        "start-subject/<int:subject_id>/",
        StartSubjectApi.as_view(),
        name="start-subject",
    ),
    path("subject-titles/", SubjectTitleApiView.as_view(), name="subject-titles"),
    path("categories/", CategoryListView.as_view(), name="categories"),
    path("steps/<int:pk>/", StepDetailAPIView.as_view(), name="step-detail"),
    path("steps/start-test/", StartStepTestView.as_view(), name="step-start-test"),
    path("clubs/", UserClubsView.as_view(), name='clubs'),
    path("club/<int:pk>/", ClubDetail.as_view(), name='club'),
    path("subject/get-test/", GetTestResultsView.as_view(), name='get_test'),
    ]
