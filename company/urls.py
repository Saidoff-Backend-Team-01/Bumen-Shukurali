from django.urls import path

from .views import *

urlpatterns = [
    path("contact/", ContactWithUsView.as_view(), name="contact_with_us"),
    path("faqs/", FAQAPIView.as_view(), name="faqs"),
]
