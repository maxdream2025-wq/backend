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
        
        # Send notification email to admin
        subject = f"New Newsletter Subscription - {instance.email}"
        message = f"""
New newsletter subscription received!

Email: {instance.email}
Subscribed at: {instance.subscribed_at}
Subscription ID: {instance.id}

This is an automated notification from your RE/MAX UAE website.
        """
        
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.NEWSLETTER_NOTIFICATION_EMAIL],
                fail_silently=False,
            )
            print(f"Newsletter subscription notification sent to {settings.NEWSLETTER_NOTIFICATION_EMAIL}")
        except Exception as e:
            print(f"Failed to send newsletter notification email: {e}")
        
        # Send welcome email to subscriber
        welcome_subject = "Welcome to RE/MAX UAE Newsletter!"
        welcome_message = f"""
Dear Subscriber,

Thank you for subscribing to the RE/MAX UAE newsletter!

We're excited to keep you updated with the latest:
• Real estate market insights
• New property listings
• Investment opportunities
• Market trends and analysis
• Exclusive offers and promotions

You'll receive our newsletter updates regularly.

Best regards,
The RE/MAX UAE Team
        """
        
        try:
            send_mail(
                subject=welcome_subject,
                message=welcome_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[instance.email],
                fail_silently=False,
            )
            print(f"Welcome email sent to {instance.email}")
        except Exception as e:
            print(f"Failed to send welcome email: {e}")
