from django.urls import path
from .views import TestimonialListCreateView, TestimonialDeleteView


urlpatterns = [
    path('testimonial/', TestimonialListCreateView.as_view(), name='testimonial-list-create'),
    path("testimonial/<int:id>/", TestimonialDeleteView.as_view(), name="testimonial-delete"),
]


