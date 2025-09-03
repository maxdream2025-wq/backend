from rest_framework import generics
from .models import CareerApplication
from .serializers import CareerApplicationSerializer
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from rest_framework.response import Response
from rest_framework import status
from django.core.files.base import ContentFile
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
import os

class CareerApplicationListCreateView(generics.ListCreateAPIView):
    queryset = CareerApplication.objects.all()
    serializer_class = CareerApplicationSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        
        # Debug logging for CV file
        print(f"CV File Debug - Instance ID: {instance.id}")
        print(f"CV File Debug - CV Resume: {instance.cv_resume}")
        print(f"CV File Debug - CV Resume Type: {type(instance.cv_resume)}")
        print(f"CV File Debug - CV Resume Name: {getattr(instance.cv_resume, 'name', 'No name attribute')}")
        
        # Send notification email to admin with CV attachment
        admin_subject = f"New Career Application - {instance.full_name}"
        admin_message = f"""
New career application received!

Applicant Details:
- Full Name: {instance.full_name}
- Email: {instance.email}
- Phone: {instance.country_code} {instance.phone}
- Applied For: {instance.applied_for}
- Description: {instance.description or 'No description provided'}
- CV/Resume: {'Attached as PDF' if instance.cv_resume else 'Not attached'}

Submitted at: {instance.created_at}

CV/Resume File: {instance.cv_resume.name if instance.cv_resume else 'No file uploaded'}

This is an automated notification from your RE/MAX UAE website.
        """
        
        try:
            if instance.cv_resume:
                # Send email with CV attachment
                email = EmailMessage(
                    subject=admin_subject,
                    body=admin_message,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[settings.CAREER_NOTIFICATION_EMAIL]
                )
                
                # Attach the CV file
                email.attach_file(instance.cv_resume.path)
                email.send()
                print(f"Career application notification with CV attachment sent to {settings.CAREER_NOTIFICATION_EMAIL}")
            else:
                # Send regular email without attachment
                send_mail(
                    subject=admin_subject,
                    message=admin_message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.CAREER_NOTIFICATION_EMAIL],
                    fail_silently=False,
                )
                print(f"Career application notification sent to {settings.CAREER_NOTIFICATION_EMAIL}")
        except Exception as e:
            print(f"Failed to send career application notification email: {e}")
            # Fallback to regular email without attachment
            try:
                send_mail(
                    subject=admin_subject,
                    message=admin_message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.CAREER_NOTIFICATION_EMAIL],
                    fail_silently=False,
                )
                print(f"Fallback email sent to {settings.CAREER_NOTIFICATION_EMAIL}")
            except Exception as fallback_error:
                print(f"Failed to send fallback email: {fallback_error}")
        
        # Send confirmation email to applicant
        applicant_subject = "Career Application Received - RE/MAX UAE"
        applicant_message = f"""
Dear {instance.first_name},

Thank you for your interest in joining the RE/MAX UAE team!

We have received your application for the position of {instance.applied_for} and our HR team will review it carefully.

Application Details:
- Position: {instance.applied_for}
- Full Name: {instance.full_name}
- Email: {instance.email}
- Phone: {instance.country_code} {instance.phone}
- CV/Resume: {'Received: ' + str(instance.cv_resume) if instance.cv_resume else 'Not received'}

Your Message: {instance.description or 'No additional message provided'}

What happens next:
1. Our HR team will review your application within 3-5 business days
2. If shortlisted, we will contact you for an interview
3. We'll keep you updated on the status of your application

Why RE/MAX UAE?
• Top-of-mind brand name in real estate
• Global network in over 110 countries
• Ongoing education and development
• Industry-leading technology tools
• Entrepreneurial freedom and support
• Unlimited growth opportunities

If you have any questions about your application, please contact us at +971 58 585 0067.

Best regards,
The RE/MAX UAE HR Team
        """
        
        try:
            send_mail(
                subject=applicant_subject,
                message=applicant_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[instance.email],
                fail_silently=False,
            )
            print(f"Career application confirmation email sent to {instance.email}")
        except Exception as e:
            print(f"Failed to send career application confirmation email: {e}")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({
                'message': 'Career application submitted successfully!',
                'application_id': serializer.instance.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def download_cv(request, application_id):
    """Download CV file for a specific application"""
    application = get_object_or_404(CareerApplication, id=application_id)
    
    if not application.cv_resume:
        raise Http404("No CV file found for this application")
    
    # Get file path and check if it exists
    file_path = application.cv_resume.path
    if not os.path.exists(file_path):
        raise Http404("CV file not found on server")
    
    # Get file extension and set appropriate content type
    file_extension = os.path.splitext(file_path)[1].lower()
    content_types = {
        '.pdf': 'application/pdf',
        '.doc': 'application/msword',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.txt': 'text/plain'
    }
    content_type = content_types.get(file_extension, 'application/octet-stream')
    
    # Read file and create response
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{application.cv_file_name}"'
        return response
