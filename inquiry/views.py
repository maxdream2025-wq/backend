from django.shortcuts import render
from rest_framework import generics
from .models import PropertyInquiry
from .serializers import PropertyInquirySerializer


# Create your views here.


class PropertyInquiryListCreateView(generics.ListCreateAPIView):
    queryset = PropertyInquiry.objects.all()
    serializer_class = PropertyInquirySerializer
