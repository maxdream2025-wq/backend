from rest_framework import serializers
from .models import PropertyInquiry
from propertyCrud.serializers import PropertySerializer


class PropertyInquirySerializer(serializers.ModelSerializer):
    property_id = serializers.IntegerField(write_only=True)
    property = PropertySerializer(read_only=True)

    class Meta:
        model = PropertyInquiry
        fields = ['id', 'property_id', 'property', 'full_name', 'email', 'phone_number', 'message', 'created_at']
        read_only_fields = ['id', 'property', 'created_at']

    def validate_property_id(self, value):
        from propertyCrud.models import Property
        try:
            Property.objects.get(id=value)
        except Property.DoesNotExist:
            raise serializers.ValidationError("Property with this ID does not exist.")
        return value

    def create(self, validated_data):
        property_id = validated_data.pop('property_id')
        from propertyCrud.models import Property
        property_obj = Property.objects.get(id=property_id)
        validated_data['property'] = property_obj
        return super().create(validated_data)
