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
        subject = f"New Contact Submission #{instance.id}"
        message = (
            f"Name: {getattr(instance, 'name', '')}\n"
            f"Email: {getattr(instance, 'email', '')}\n"
            f"Phone: {getattr(instance, 'phone', '')}\n"
            f"Message: {getattr(instance, 'message', '')}\n"
            f"Submitted At: {getattr(instance, 'submitted_at', '')}"
        )
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_TO_SALES],
                fail_silently=True,
            )
        except Exception:
            # Silently ignore; API success should not fail due to email
            pass

def contact_table(request):
    contacts = ContactSubmission.objects.all().order_by('-submitted_at')
    return render(request, 'contact_table.html', {'contacts': contacts})
