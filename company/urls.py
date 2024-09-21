from django.urls import path

from .views import *

urlpatterns = [
    path("contact_with_us/", ContactWithUsView.as_view(), name="contact_with_us"),
    path("faqs/", FAQAPIView.as_view(), name="faqs"),
    path('contact/', ContactsDetailView.as_view(), name="contact"),
    path('privacy_policy/', PrivacyPolicyView.as_view(), name="privacy_policy")
    path("contact/", ContactsDetailView.as_view(), name="contact"),
    path("advertisements/", AdvertisingListView.as_view(), name="advertisements-list"),
]
