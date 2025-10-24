#!/usr/bin/env python
"""
Simple Email Test Script for RE/MAX Project
"""

import os
import sys
import django
from django.conf import settings
from django.core.mail import send_mail

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'property.settings')
django.setup()

def test_email():
    """Test sending a simple email"""
    try:
        print("=== RE/MAX Email Test ===")
        print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
        print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
        print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
        print(f"CONTACT_NOTIFICATION_EMAIL: {settings.CONTACT_NOTIFICATION_EMAIL}")
        print()
        
        subject = "RE/MAX Email Test - Configuration Updated"
        message = """
        This is a test email from RE/MAX backend.
        
        Email configuration has been updated:
        - From: info@remaxdreamuae.com
        - To: info@remaxdreamuae.com
        - CC emails removed
        - All notifications now go to info email
        
        If you receive this email, the configuration is working correctly.
        """
        
        recipient_list = [settings.CONTACT_NOTIFICATION_EMAIL]
        
        print(f"Sending test email to: {recipient_list}")
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        
        print("SUCCESS: Test email sent successfully!")
        print(f"Email sent to: {recipient_list}")
        print("Check your inbox at info@remaxdreamuae.com")
        
    except Exception as e:
        print(f"ERROR: Failed to send test email: {e}")
        print("Please check your email configuration and credentials.")
        return False
    
    return True

if __name__ == "__main__":
    test_email()
