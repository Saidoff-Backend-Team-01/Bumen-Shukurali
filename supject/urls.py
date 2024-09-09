from django.urls import path

from .views import (
    CategoryAPIView,
    CategoryListView,
    ClubDetail,
    GetTestResultsView,
    StartStepTestView,
    StartSubjectApi,
    StepDetailAPIView,
    SubjectSearchApiView,
    SubjectTitleApiView,
    UserClubsView,
    UserPopularSubject,
    TopUserList,
)

urlpatterns = [
    path("category/<int:pk>/", CategoryAPIView.as_view(), name="category-subject"),
    path(
        "start-subject/<int:subject_id>/",
        StartSubjectApi.as_view(),
        name="start-subject",
    ),
    path("subject-titles/", SubjectTitleApiView.as_view(), name="subject-titles"),
    path(
        "userpopularsubject/", UserPopularSubject.as_view(), name="userpopularsubject"
    ),
    path("categories/", CategoryListView.as_view(), name="categories"),
    path("steps/<int:pk>/", StepDetailAPIView.as_view(), name="step-detail"),
    path("steps/start-test/", StartStepTestView.as_view(), name="step-start-test"),
    path("subject-search/", SubjectSearchApiView.as_view(), name="subject-search"),
    path("clubs/", UserClubsView.as_view(), name="clubs"),
    path("club/<int:pk>/", ClubDetail.as_view(), name="club"),
    path("subject/get-test/", GetTestResultsView.as_view(), name="get_test"),
    path(
        "user-popular_subjects/",
        UserPopularSubject.as_view(),
        name="user-popular-subjects",

    ),
    path("tops/", TopUserList.as_view(), name='tops'),


]
