from django.shortcuts import render
from rest_framework import generics
from .models import Newsletter
from .serializers import NewsletterSerializer

# Create your views here.

class NewsletterListCreateView(generics.ListCreateAPIView):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
