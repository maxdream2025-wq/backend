from django.urls import path
from .views import CareerApplicationListCreateView, download_cv

urlpatterns = [
    path('', CareerApplicationListCreateView.as_view(), name='career-application-list-create'),
    path('download-cv/<int:application_id>/', download_cv, name='download-cv'),
]
