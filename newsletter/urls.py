from django.urls import path
from .views import NewsletterListCreateView, send_test_email

urlpatterns = [
    path('', NewsletterListCreateView.as_view(), name='newsletter-list-create'),
    path('test-email/', send_test_email, name='newsletter-test-email'),
]