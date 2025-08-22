from django.urls import path
from .views import PropertyInquiryListCreateView


urlpatterns = [
    path('inquiry/', PropertyInquiryListCreateView.as_view(), name='inquiry-list-create'),
]
