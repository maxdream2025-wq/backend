from rest_framework import generics
from .models import ContactSubmission
from .serializer import ContactSubmissionSerializer
from django.shortcuts import render

class ContactSubmissionListCreateView(generics.ListCreateAPIView):
    queryset = ContactSubmission.objects.all().order_by('-submitted_at')
    serializer_class = ContactSubmissionSerializer

def contact_table(request):
    contacts = ContactSubmission.objects.all().order_by('-submitted_at')
    return render(request, 'contact_table.html', {'contacts': contacts})
