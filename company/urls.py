from django.urls import path

from .views import *

urlpatterns = [
    path("contact_with_us/", ContactWithUsView.as_view(), name="contact_with_us"),
    path("faqs/", FAQAPIView.as_view(), name="faqs"),
    path('contact/', ContactsDetailView.as_view(), name="contact"),
    path('privacy_policy/', PrivacyPolicyView.as_view(), name="privacy_policy"),
    path("advertisements/", AdvertisingListView.as_view(), name="advertisements-list"),
    path("app_info/", AppInfoView.as_view(), name="app_info"),
    path("sponsors/", SponsorsView.as_view(), name="sponsors"),
    path('contact_with_us_categories/', ContactWithUsCategoryAPIView.as_view(), name='contact_with_us_categories'),
    path('contact_with_us_reasons/', ContactWithUsReasonAPIView.as_view(), name='contact_with_us_reasons'),
    path('contact_with_us_submit/', ContactWithUsMobileAPIView.as_view(), name='contact_with_us_submit')
]