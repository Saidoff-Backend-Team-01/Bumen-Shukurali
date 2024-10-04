from django.urls import path

from .views import (
    CategoryAPIView,
    CategoryListView,
    ClubDetail,
    GetTestResultsView,
    JoinDiscussionGroupView,
    StartStepTestView,
    StartSubjectApi,
    StepDetailAPIView,
    StepTestFinishView,
    SubjectSearchApiView,
    SubmitTestView,
    TopUserList,
    UserClubsView,
    UserPopularSubject,
    JoinDiscussionGroupView,
    TopUserList,
    UserSubjectListApiView,
)

urlpatterns = [
    path("category/<int:pk>/", CategoryAPIView.as_view(), name="category-subject"),
    path(
        "start-subject/<int:subject_id>/",
        StartSubjectApi.as_view(),
        name="start-subject",
    ),
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
    path(
        "join_group/<int:user_id>/<int:subject_id>/",
        JoinDiscussionGroupView.as_view(),
        name="join_group",
    ),
    path("tops/", TopUserList.as_view(), name="tops"),
    path("user-subjects/", UserSubjectListApiView.as_view(), name="user-subjects"),
    path("step-test/submit/", SubmitTestView.as_view(), name="submit-test"),
    path("finish-step-test/", StepTestFinishView.as_view(), name="finish-step-test"),
]