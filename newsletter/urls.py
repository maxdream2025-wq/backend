from django.urls import path
from .views import NewsletterListCreateView

urlpatterns = [
    path('', NewsletterListCreateView.as_view(), name='newsletter-list-create'),
]