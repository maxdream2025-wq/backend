from django.shortcuts import render
from rest_framework import generics
from .models import Newsletter
from .serializers import NewsletterSerializer
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.

class NewsletterListCreateView(generics.ListCreateAPIView):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        subject = f"New Newsletter Subscription #{instance.id}"
        message = f"Email: {getattr(instance, 'email', '')}"
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_TO_NEWSLETTER],
                fail_silently=True,
            )
        except Exception:
            pass
