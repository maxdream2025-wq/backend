from django.urls import path
from .views import ContactSubmissionListCreateView, contact_table

urlpatterns = [
    path('', ContactSubmissionListCreateView.as_view(), name='contact-list-create'),
    path('table/', contact_table, name='contact-table'),
]