from .models import CustomUser,Review,Profile , Myhome, Category ,Property, Review,MaintenanceRequest, TenantApplication, Payment
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__' 


class CustomUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only = True)
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {"password":{"write_only":True}}
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        
        # Ensure Profile is not duplicated
        profile, created = Profile.objects.get_or_create(user=user)
        return user

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = '__all__'
        
class PropertySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only = True)
    landlord = CustomUserSerializer(read_only=True)
    class Meta:
        model = Property
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class MaintenanceRequestSerializer(serializers.ModelSerializer):
    property = PropertySerializer(read_only = True)
    tenant = CustomUserSerializer(read_only = True)
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
    
class MyHomeSerializer(serializers.ModelSerializer):
    property = PropertySerializer(read_only=True)  # Use nested serializer for property details
    tenant = CustomUserSerializer(read_only=True)
    class Meta:
        model = Myhome
        fields = ['id','property','tenant']

class MyPropertySerializer(serializers.ModelSerializer):
    landlord = CustomUserSerializer(read_only=True)
    tenant = CustomUserSerializer(read_only=True)
    class Meta:
        model = Property
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Payment
        fields = ['amount', 'currency', 'stripe_payment_id', 'property', 'tenant']