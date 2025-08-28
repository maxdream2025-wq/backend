from django.shortcuts import render
from rest_framework import generics
from .models import PropertyInquiry
from .serializers import PropertyInquirySerializer
from django.conf import settings
from django.core.mail import send_mail


# Create your views here.


class PropertyInquiryListCreateView(generics.ListCreateAPIView):
    queryset = PropertyInquiry.objects.all()
    serializer_class = PropertyInquirySerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        subject = f"New Property Inquiry #{instance.id}"
        message = (
            f"Name: {getattr(instance, 'name', '')}\n"
            f"Email: {getattr(instance, 'email', '')}\n"
            f"Phone: {getattr(instance, 'phone', '')}\n"
            f"Property: {getattr(instance, 'property_title', '')} (ID: {getattr(instance, 'property_id', '')})\n"
            f"Message: {getattr(instance, 'message', '')}"
        )
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_TO_INQUIRY],
                fail_silently=True,
            )
        except Exception:
            pass
