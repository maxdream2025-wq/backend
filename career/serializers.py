from rest_framework import serializers
from .models import CareerApplication

class CareerApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerApplication
        fields = [
            'id', 'first_name', 'last_name', 'email', 'country_code', 
            'phone', 'cv_resume', 'description', 'applied_for', 
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Set default applied_for if not provided
        if 'applied_for' not in validated_data:
            validated_data['applied_for'] = 'Real Estate Agent'
        return super().create(validated_data)
