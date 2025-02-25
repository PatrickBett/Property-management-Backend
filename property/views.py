from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
import stripe
from rest_framework import serializers

from django.conf import settings
from django.http import JsonResponse
import json
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.views.decorators.csrf import csrf_exempt
from .models import Property,Category ,CustomUser, Myhome ,Review, MaintenanceRequest, TenantApplication
from .serializers import (
    PropertySerializer,
    MyPropertySerializer,
    CustomUserSerializer,
    MyHomeSerializer,
    ReviewSerializer,
    MaintenanceRequestSerializer,
    TenantApplicationSerializer, 
    CategorySerializer,
    CustomTokenObtainPairSerializer
)
# from .permissions import IsTenant, IsLandlord  # Assuming you have custom permissions


# CustomUser ViewSet
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    

    def get_queryset(self):
        # Filter by role if a query parameter is provided
        role = self.request.query_params.get('role')
        if role:
            return CustomUser.objects.filter(role=role)
        return CustomUser.objects.all()
# View to retrieve a certain user 
class CustomUserListView(generics.RetrieveAPIView):
    serializer_class=CustomUserSerializer
    permission_classes =[IsAuthenticated]

    def get_object(self):
        return self.request.user
# Categories
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


# Property Views
class PropertyListView(generics.ListCreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        category_id = self.request.data.get("category")  # Get category from request data
        category = None
        if category_id:
            try:
                category = Category.objects.get(id=category_id)  # Fetch the category instance
            except Category.DoesNotExist:
                raise serializers.ValidationError({"category": "Invalid category ID"})

        serializer.save(landlord=self.request.user, category=category)



class PropertyDestroyView(generics.DestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]  # Only landlords can delete properties


class PropertyUpdateView(generics.UpdateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]  # Only landlords can update properties

    def get_object(self):
        return super().get_object()


# Tenant Dashboard View
class TenantDashboardView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]  # Custom permission for tenants

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



stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def create_payment_intent(request):
    """
    Create a PaymentIntent for Stripe payments.
    """
    if request.method == "POST":
        try:
            # Parse the JSON body
            data = json.loads(request.body)
            amount = data.get("amount")  # Get the 'amount' from the request body

            if not amount or amount <= 0:
                return JsonResponse({"error": "Invalid amount"}, status=400)

            # Create a PaymentIntent
            intent = stripe.PaymentIntent.create(
                amount=amount,  # Amount in cents
                currency="usd",
                payment_method_types=["card"],
            )

            return JsonResponse({"clientSecret": intent["client_secret"]})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        
class MyHomeListCreateView(ListCreateAPIView):
    """
    Handles listing all MyHome objects and creating a new one.
    Supports optional filtering by tenant_id using query parameters.
    """
    serializer_class = MyHomeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter homes by the authenticated tenant
        return Myhome.objects.filter(tenant=self.request.user)


class MyHomeRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    Handles retrieving, updating, and deleting a specific MyHome object.
    """
    queryset = Myhome.objects.all()
    serializer_class = MyHomeSerializer 
    permission_classes = [IsAuthenticated]      



class MyPropertyListCreateView(ListCreateAPIView):

    serializer_class = MyPropertySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter property by the authenticated landlord
        return Property.objects.filter(landlord=self.request.user)
    

class MaintenanceRequestCreateListView(generics.ListCreateAPIView):
    """
    API view to list all maintenance requests and allow tenants to create new requests.
    """
    queryset = MaintenanceRequest.objects.all()
    serializer_class = MaintenanceRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Ensure tenants can only see their own maintenance requests.
        """
        user = self.request.user
        if user.role == "tenant":
            return MaintenanceRequest.objects.filter(tenant=user)
        return MaintenanceRequest.objects.none()  # Return an empty queryset for non-tenants

    def perform_create(self, serializer):
        """
        Automatically set the tenant field to the logged-in user when creating a request.
        """
        serializer.save(tenant=self.request.user)