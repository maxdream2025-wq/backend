# property/views.py

from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import PropertyCategory, Property
from .serializers import PropertyCategorySerializer, PropertySerializer
from django.db.models import Q
from decimal import Decimal

# For CRUD on category
class PropertyCategoryViewSet(viewsets.ModelViewSet):
    queryset = PropertyCategory.objects.all().order_by('order')
    serializer_class = PropertyCategorySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        developer_param = self.request.query_params.get('developer')
        if developer_param is not None:
            val = developer_param.strip().lower()
            if val in {"true", "1", "yes"}:
                queryset = queryset.filter(developer=True)
            elif val in {"false", "0", "no"}:
                queryset = queryset.filter(developer=False)
        return queryset


# For CRUD on property
class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    def create(self, request, *args, **kwargs):
        # Support both single-object and array payloads on /property/
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers({})
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=["post"], url_path="bulk")
    def bulk_create(self, request, *args, **kwargs):
        # Accepts a JSON array of property objects (application/json)
        if not isinstance(request.data, list):
            return Response(
                {"detail": "Expected a JSON array."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers({})
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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
                Q(location__icontains=location)
                | Q(category__title__icontains=location)
                | Q(category__property_category__icontains=location)
                | Q(category__slug__icontains=location)
            )

        # Apply optional filters
        if property_type:
            queryset = queryset.filter(property_type__icontains=property_type)

        if user_type:
            # user_type stored as CharField (e.g., "Investor,End User")
            queryset = queryset.filter(user_type__icontains=user_type)

        if bedroom:
            # bedroom stored as CSV string; use icontains for simple match
            queryset = queryset.filter(bedroom__icontains=bedroom)

        if bathroom:
            # bathroom stored as CSV string; use icontains for simple match
            queryset = queryset.filter(bathroom__icontains=bathroom)

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
