from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
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
                # cc=[settings.CC_EMAIL],  # Removed CC email
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


@api_view(["POST", "GET"])  # Allow quick testing via GET or POST
@permission_classes([AllowAny])
def send_test_email(request):
    """Send a single test email to all configured notification addresses.

    Optional query/body param:
      - to: extra recipient email to include in the test
    """
    extra_to = request.data.get("to") if hasattr(request, "data") else None
    if not extra_to:
        extra_to = request.query_params.get("to")

    recipients = {
        getattr(settings, "EMAIL_HOST_USER", None),
        getattr(settings, "NEWSLETTER_NOTIFICATION_EMAIL", None),
        getattr(settings, "INQUIRY_NOTIFICATION_EMAIL", None),
        getattr(settings, "CONTACT_NOTIFICATION_EMAIL", None),
        getattr(settings, "CAREER_NOTIFICATION_EMAIL", None),
        # getattr(settings, "CC_EMAIL", None),  # Removed CC email
        extra_to,
    }
    recipients = [r for r in recipients if r]

    if not recipients:
        return Response(
            {"ok": False, "error": "No recipients configured."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    subject = "RE/MAX Email Test"
    message = (
        "This is a test email to verify SMTP configuration on RE/MAX backend.\n\n"
        f"Environment DEBUG={getattr(settings, 'DEBUG', None)}"
    )

    try:
        sent_count = send_mail(
            subject=subject,
            message=message,
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", getattr(settings, "EMAIL_HOST_USER", None)),
            recipient_list=recipients,
            fail_silently=False,
        )
        return Response(
            {"ok": True, "attempted": recipients, "sent_count": sent_count},
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        return Response(
            {"ok": False, "attempted": recipients, "error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
