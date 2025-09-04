from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Testimonial
from .serializers import TestimonialSerializer, TestimonialAdminSerializer


class TestimonialListCreateView(generics.ListCreateAPIView):
    queryset = Testimonial.objects.filter(approval_status='approved')
    serializer_class = TestimonialSerializer

    def perform_create(self, serializer):
        testimonial = serializer.save()
        # Send email notification to admin
        self.send_review_notification(testimonial)

    def send_review_notification(self, testimonial):
        try:
            subject = f'New Review Submission from {testimonial.name}'
            
            # Create HTML email content
            html_message = f"""
            <html>
            <body>
                <h2>New Review Submission</h2>
                <p><strong>Name:</strong> {testimonial.name}</p>
                <p><strong>Email:</strong> {testimonial.email or 'Not provided'}</p>
                <p><strong>Rating:</strong> {testimonial.rating}/5</p>
                <p><strong>Review:</strong></p>
                <p style="background-color: #f5f5f5; padding: 10px; border-left: 4px solid #007bff;">
                    {testimonial.text}
                </p>
                <p><strong>Submitted:</strong> {testimonial.created_at.strftime('%Y-%m-%d %H:%M:%S')}</p>
                
                <hr>
                <p><strong>Admin Actions:</strong></p>
                <p>Please login to admin panel to review and approve this testimonial:</p>
                <p><a href="{settings.FRONTEND_URL}/admin/login" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px; display: inline-block;">Go to Admin Panel</a></p>
                
                <p><strong>Review ID:</strong> #{testimonial.id}</p>
                <p><strong>Reviewer:</strong> {testimonial.name}</p>
            </body>
            </html>
            """
            
            plain_message = strip_tags(html_message)
            
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_NOTIFICATION_EMAIL],
                html_message=html_message,
                fail_silently=False,
            )
        except Exception as e:
            print(f"Failed to send email notification: {e}")


class TestimonialDeleteView(generics.DestroyAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    lookup_field = "id"


class TestimonialAdminListView(generics.ListAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialAdminSerializer


class TestimonialAdminUpdateView(generics.UpdateAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialAdminSerializer
    lookup_field = "id"


@api_view(['POST'])
def approve_testimonial(request, testimonial_id):
    try:
        testimonial = Testimonial.objects.get(id=testimonial_id)
        testimonial.approval_status = 'approved'
        testimonial.admin_notes = request.data.get('admin_notes', '')
        testimonial.save()
        
        # Send approval email to user if email is provided
        if testimonial.email:
            try:
                subject = 'Your Review Has Been Approved - ReMax'
                html_message = f"""
                <html>
                <body>
                    <h2>Review Approved!</h2>
                    <p>Dear {testimonial.name},</p>
                    <p>Thank you for your review! We're happy to inform you that your review has been approved and is now visible on our website.</p>
                    
                    <p><strong>Your Review:</strong></p>
                    <p style="background-color: #f5f5f5; padding: 10px; border-left: 4px solid #28a745;">
                        "{testimonial.text}"
                    </p>
                    <p><strong>Rating:</strong> {testimonial.rating}/5 stars</p>
                    
                    <p>Thank you for taking the time to share your experience with us!</p>
                    <p>Best regards,<br>ReMax Team</p>
                </body>
                </html>
                """
                
                plain_message = strip_tags(html_message)
                
                send_mail(
                    subject=subject,
                    message=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[testimonial.email],
                    html_message=html_message,
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Failed to send approval email: {e}")
        
        return Response({'message': 'Testimonial approved successfully'}, status=status.HTTP_200_OK)
    except Testimonial.DoesNotExist:
        return Response({'error': 'Testimonial not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def reject_testimonial(request, testimonial_id):
    try:
        testimonial = Testimonial.objects.get(id=testimonial_id)
        testimonial.approval_status = 'rejected'
        testimonial.admin_notes = request.data.get('admin_notes', '')
        testimonial.save()
        
        # Send rejection email to user if email is provided
        if testimonial.email:
            try:
                subject = 'Review Update - ReMax'
                html_message = f"""
                <html>
                <body>
                    <h2>Review Update</h2>
                    <p>Dear {testimonial.name},</p>
                    <p>Thank you for your review submission. After careful consideration, we have decided not to publish your review at this time.</p>
                    
                    <p>This could be due to various reasons such as:</p>
                    <ul>
                        <li>Content that doesn't meet our community guidelines</li>
                        <li>Inappropriate language or content</li>
                        <li>Duplicate or spam content</li>
                    </ul>
                    
                    <p>We encourage you to submit another review that follows our guidelines.</p>
                    <p>Thank you for your understanding.</p>
                    <p>Best regards,<br>ReMax Team</p>
                </body>
                </html>
                """
                
                plain_message = strip_tags(html_message)
                
                send_mail(
                    subject=subject,
                    message=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[testimonial.email],
                    html_message=html_message,
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Failed to send rejection email: {e}")
        
        return Response({'message': 'Testimonial rejected successfully'}, status=status.HTTP_200_OK)
    except Testimonial.DoesNotExist:
        return Response({'error': 'Testimonial not found'}, status=status.HTTP_404_NOT_FOUND)