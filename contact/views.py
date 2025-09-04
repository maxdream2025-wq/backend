from rest_framework import generics
from .models import ContactSubmission
from .serializer import ContactSubmissionSerializer
from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail

class ContactSubmissionListCreateView(generics.ListCreateAPIView):
    queryset = ContactSubmission.objects.all().order_by('-submitted_at')
    serializer_class = ContactSubmissionSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        
        # Send notification email to admin
        subject = f"New Contact Form Submission - {instance.help_category}"
        message = f"""
New contact form submission received!

Help Category: {instance.help_category}

Customer Details:
- Full Name: {instance.first_name} {instance.last_name}
- Email: {instance.email}
- Country Code: {instance.country_code}
- Phone: {instance.phone}
- Message: {instance.message}

Submitted at: {instance.submitted_at}

This is an automated notification from your RE/MAX UAE website.
        """
        
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.CONTACT_NOTIFICATION_EMAIL],
                fail_silently=False,
                cc=[settings.CC_EMAIL],
            )
            print(f"Contact form notification sent to {settings.CONTACT_NOTIFICATION_EMAIL}")
        except Exception as e:
            print(f"Failed to send contact form notification email: {e}")
        
        # Send confirmation email to customer
        customer_subject = "Thank you for contacting RE/MAX UAE!"
        customer_message = f"""
Dear {instance.first_name} {instance.last_name},

Thank you for contacting RE/MAX UAE!

We have received your message regarding: {instance.help_category}

Your Message: {instance.message}

Our team will review your inquiry and get back to you within 24 hours.

Contact Information:
- Email: {instance.email}
- Phone: {instance.country_code} {instance.phone}

If you have any urgent questions, please call us at +971 58 585 0067.

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
            print(f"Contact form confirmation email sent to {instance.email}")
        except Exception as e:
            print(f"Failed to send contact form confirmation email: {e}")

def contact_table(request):
    contacts = ContactSubmission.objects.all().order_by('-submitted_at')
    return render(request, 'contact_table.html', {'contacts': contacts})
