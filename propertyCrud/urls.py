from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PropertyCategoryViewSet,
    PropertyViewSet,
    PropertyDetailView,
    PropertyByCategorySlugView,
    FindPropertyView,
)

router = DefaultRouter()
router.register(r'property-categories', PropertyCategoryViewSet)
router.register(r'property', PropertyViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),

    # single property by its slug
    path("v1/property/<slug:slug>/", PropertyDetailView.as_view(), name="property-detail-slug"),

    # all properties under category slug
    path("v1/category/<slug:slug>/properties/", PropertyByCategorySlugView.as_view(), name="properties-by-category"),

    # find properties with filters
    path("v1/find-property/", FindPropertyView.as_view(), name="find-property"),
]
