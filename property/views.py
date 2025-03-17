from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
import stripe
from rest_framework import serializers
from django.shortcuts import get_object_or_404

from django.conf import settings
from django.http import JsonResponse
import json
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.views.decorators.csrf import csrf_exempt
from .models import (Property,Category ,
                     CustomUser, Myhome ,
                     Review, MaintenanceRequest, 
                     TenantApplication,
                     Profile,
                     Payment)

from .serializers import (
    PropertySerializer,
    MyPropertySerializer,
    CustomUserSerializer,
    MyHomeSerializer,
    ReviewSerializer,
    MaintenanceRequestSerializer,
    TenantApplicationSerializer, 
    CategorySerializer,
    CustomTokenObtainPairSerializer,
    PaymentSerializer
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


class PropertyUpdateView(generics.UpdateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_available = False
        instance.tenant = CustomUser.objects.get(id=request.data['tenant_id'])
        instance.save()
        return Response({"message": "Property updated successfully"})
    

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

# Payment listing view
class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset= Payment.objects.all()




# Create Payment Intent for stripe payments
stripe.api_key = settings.STRIPE_SECRET_KEY

class CreatePaymentIntentView(APIView):
    def post(self,request):
        amount = request.data.get("amount")
        currency = request.data.get("currency")
        property_id = request.data.get("property_id")
        # property = get_object_or_404(Property, id=property_id)
        tenant = self.request.user


        # Fetch the property instance using Property.objects.get(id=property_id)
        try:
            # property = Property.objects.get(id=property_id)
            property = get_object_or_404(Property, id=property_id)
            
        except Property.DoesNotExist:
            return Response({'error': 'Property not found'}, status=404)

# basic validations
        
        if not currency:
            return Response({'error':'Currency is required'}, status=400)

        try:
            intent = stripe.PaymentIntent.create(
                amount = int(float(request.data.get("amount"))*100),
                currency=currency,
                metadata={
                'property_id': property.id,  # Adding property.id as metadata
    }
            )

            # save to the database

            payment_data = {
                'amount': amount,
                'currency': currency,
                'stripe_payment_id': intent['id'],
                'property':property.id,
                'tenant':tenant.id              
            }
            print("INTENT  METADATA",intent.metadata.property_id)
            
            serializer = PaymentSerializer(data=payment_data)

            if serializer.is_valid():

                serializer.save(tenant=tenant,property=property)
                # payment_confirmation = stripe.PaymentIntent.retrieve(intent["id"])
                
                # property.is_available = False
                # property.tenant = tenant
                # property.save()
                # myhome = Myhome.objects.create(property=property, tenant=tenant)

                # if payment_confirmation.status == "succeeded":
                    
                #     property.is_available = False
                #     property.tenant = tenant
                #     property.save()
                #     myhome = Myhome.objects.create(property=property, tenant=tenant)

                
                return Response(
                    {
                        'clientSecret':intent['client_secret'],
                        'payment': serializer.data,
                    },
                )
            
            return Response(serializer.errors)


        except stripe.error.StripeError as e:
            return Response({
                'error': str(e)
            })


class FinalyzePayment(APIView):
    def post(self,request):
        payment_intent_id = request.data.get("paymentIntentId")
        property_id = request.data.get("property_id")
        property = get_object_or_404(Property, id=property_id)
        paymentConfirmation = stripe.PaymentIntent.retrieve(payment_intent_id)

        if paymentConfirmation.status == "succeeded":
            property.is_available = False
            property.tenant = self.request.user
            property.save()
            Myhome.objects.create(property=property, tenant=self.request.user)

        return Response({'message': 'Payment successful and property updated'})


    
