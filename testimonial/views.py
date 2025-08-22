from rest_framework import generics
from .models import Testimonial
from .serializers import TestimonialSerializer


class TestimonialListCreateView(generics.ListCreateAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer

from django.shortcuts import render

# Create your views here.
