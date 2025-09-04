from django.urls import path
from .views import (
    TestimonialListCreateView, 
    TestimonialDeleteView,
    TestimonialAdminListView,
    TestimonialAdminUpdateView,
    approve_testimonial,
    reject_testimonial
)


urlpatterns = [
    path('testimonial/', TestimonialListCreateView.as_view(), name='testimonial-list-create'),
    path("testimonial/<int:id>/", TestimonialDeleteView.as_view(), name="testimonial-delete"),
    path('admin/testimonials/', TestimonialAdminListView.as_view(), name='testimonial-admin-list'),
    path('admin/testimonials/<int:id>/', TestimonialAdminUpdateView.as_view(), name='testimonial-admin-update'),
    path('admin/testimonials/<int:testimonial_id>/approve/', approve_testimonial, name='approve-testimonial'),
    path('admin/testimonials/<int:testimonial_id>/reject/', reject_testimonial, name='reject-testimonial'),
]


