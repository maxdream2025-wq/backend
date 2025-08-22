from django.urls import path
from .views import TestimonialListCreateView


urlpatterns = [
    path('testimonial/', TestimonialListCreateView.as_view(), name='testimonial-list-create'),
]


