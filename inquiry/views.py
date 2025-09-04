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
        
        # Send notification email to admin
        subject = f"New Property Interest - {instance.property.property_name}"
        message = f"""
New property interest registration received!

Property: {instance.property.property_name}
Property ID: {instance.property.id}
Location: {instance.property.location}

Customer Details:
- Full Name: {instance.full_name}
- Email: {instance.email}
- Phone: {instance.phone_number}
- Message: {instance.message}

Submitted at: {instance.created_at}

This is an automated notification from your RE/MAX UAE website.
        """
        
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.INQUIRY_NOTIFICATION_EMAIL],
                fail_silently=False,
                cc=[settings.CC_EMAIL],
            )
            print(f"Property inquiry notification sent to {settings.INQUIRY_NOTIFICATION_EMAIL}")
        except Exception as e:
            print(f"Failed to send property inquiry notification email: {e}")
        
        # Send confirmation email to customer
        customer_subject = f"Interest Registered - {instance.property.property_name}"
        customer_message = f"""
Dear {instance.full_name},

Thank you for registering your interest in {instance.property.property_name}!

We have received your inquiry and our team will contact you shortly with more details about this property.

Property Details:
- Name: {instance.property.property_name}
- Location: {instance.property.location}
- Property Type: {instance.property.property_type}
- Starting Price: AED {instance.property.starting_price} M

Your Message: {instance.message}

Our team will review your requirements and get back to you within 24 hours.

Best regards,
The RE/MAX UAE Team
        """
        
        try:
            send_mail(
                subject=customer_subject,
                message=customer_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[instance.email],
                fail_silently=False,
            )
            print(f"Confirmation email sent to {instance.email}")
        except Exception as e:
            print(f"Failed to send confirmation email: {e}")
