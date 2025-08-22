# property/views.py

from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from .models import PropertyCategory, Property
from .serializers import PropertyCategorySerializer, PropertySerializer
from django.db.models import Q
from decimal import Decimal

# For CRUD on category
class PropertyCategoryViewSet(viewsets.ModelViewSet):
    queryset = PropertyCategory.objects.all()
    serializer_class = PropertyCategorySerializer


# For CRUD on property
class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer


# Single property by slug
class PropertyDetailView(generics.RetrieveAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    lookup_field = "slug"


# All properties by category slug
class PropertyByCategorySlugView(generics.ListAPIView):
    serializer_class = PropertySerializer

    def get_queryset(self):
        category_slug = self.kwargs["slug"]
        return Property.objects.filter(category__slug=category_slug)


class FindPropertyView(generics.ListAPIView):
    serializer_class = PropertySerializer

    def get(self, request, *args, **kwargs):
        # Check if location is provided
        location = request.query_params.get('location', None)
        if not location:
            return Response(
                {"error": "Location is required. Please provide a location parameter."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Property.objects.all()

        # Get query parameters
        location = self.request.query_params.get('location', None)
        property_type = self.request.query_params.get('propertyType', None)
        user_type = self.request.query_params.get('userType', None)
        bedroom = self.request.query_params.get('bedroom', None)
        bathroom = self.request.query_params.get('bathroom', None)
        completion_status = self.request.query_params.get('completionStatus', None)
        min_price = self.request.query_params.get('minPrice', None)
        max_price = self.request.query_params.get('maxPrice', None)
        area_min = self.request.query_params.get('areaMin', None)
        area_max = self.request.query_params.get('areaMax', None)

        # Apply location filter (required)
        if location:
            queryset = queryset.filter(
                Q(location__icontains=location) | 
                Q(location_search__icontains=location)
            )

        # Apply optional filters
        if property_type:
            queryset = queryset.filter(property_type__icontains=property_type)

        if user_type:
            queryset = queryset.filter(user_type__contains=[user_type])

        if bedroom:
            queryset = queryset.filter(bedroom__contains=[bedroom])

        if bathroom:
            queryset = queryset.filter(bathroom__contains=[bathroom])

        if completion_status:
            queryset = queryset.filter(status__icontains=completion_status)

        if min_price:
            try:
                min_price_decimal = Decimal(min_price)
                queryset = queryset.filter(starting_price__gte=min_price_decimal)
            except (ValueError, TypeError):
                pass

        if max_price:
            try:
                max_price_decimal = Decimal(max_price)
                queryset = queryset.filter(starting_price__lte=max_price_decimal)
            except (ValueError, TypeError):
                pass

        if area_min:
            try:
                area_min_int = int(area_min)
                queryset = queryset.filter(area__min__gte=area_min_int)
            except (ValueError, TypeError):
                pass

        if area_max:
            try:
                area_max_int = int(area_max)
                queryset = queryset.filter(area__max__lte=area_max_int)
            except (ValueError, TypeError):
                pass

        return queryset.order_by('-starting_price')
