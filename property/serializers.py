from .models import CustomUser,Review, Property, Review,MaintenanceRequest, TenantApplication
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {"password":{"write_only":True}}
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

        
class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class MaintenanceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceRequest
        fields = '__all__'

class TenantApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantApplication
        fields = '__all__'

# To alter the tokenobtainview
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Add custom claims to the response
        data['role'] = self.user.role  # Assuming your user model has a `role` field
        return data