from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Property, CustomUser, Review, MaintenanceRequest, TenantApplication
from .serializers import (
    PropertySerializer,
    CustomUserSerializer,
    ReviewSerializer,
    MaintenanceRequestSerializer,
    TenantApplicationSerializer, 
    CustomTokenObtainPairSerializer
)
# from .permissions import IsTenant, IsLandlord  # Assuming you have custom permissions


# CustomUser ViewSet
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter by role if a query parameter is provided
        role = self.request.query_params.get('role')
        if role:
            return CustomUser.objects.filter(role=role)
        return CustomUser.objects.all()


# Property Views
class PropertyListView(generics.ListCreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    # permission_classes = [IsAuthenticated]


class PropertyDestroyView(generics.DestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    lookup_field = 'pk'
    # permission_classes = [IsAuthenticated]  # Only landlords can delete properties


class PropertyUpdateView(generics.UpdateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    lookup_field = 'pk'
    # permission_classes = [IsAuthenticated]  # Only landlords can update properties

    def get_object(self):
        return super().get_object()


# Tenant Dashboard View
class TenantDashboardView(generics.GenericAPIView):
    # permission_classes = [IsAuthenticated]  # Custom permission for tenants

    def get(self, request, *args, **kwargs):
        user = request.user
        rented_properties = Property.objects.filter(tenants=user)
        maintenance_requests = MaintenanceRequest.objects.filter(tenant=user)

        return Response({
            "user": CustomUserSerializer(user).data,
            "rented_properties": PropertySerializer(rented_properties, many=True).data,
            "maintenance_requests": MaintenanceRequestSerializer(maintenance_requests, many=True).data,
        })


# Landlord Dashboard View
class LandlordDashboardView(generics.GenericAPIView):
    # permission_classes = [IsAuthenticated]  # Custom permission for landlords

    def get(self, request, *args, **kwargs):
        user = request.user
        owned_properties = Property.objects.filter(owner=user)
        tenant_applications = TenantApplication.objects.filter(property__owner=user)

        return Response({
            "user": CustomUserSerializer(user).data,
            "owned_properties": PropertySerializer(owned_properties, many=True).data,
            "tenant_applications": TenantApplicationSerializer(tenant_applications, many=True).data,
        })
    
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

