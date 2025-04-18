from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.views import APIView
import base64
from django.core.files.base import ContentFile
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
import stripe
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
from django.http import JsonResponse
import json
from .utils import upload_file_to_s3
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.views.decorators.csrf import csrf_exempt
from .models import (Property,Category ,
                     CustomUser, Myhome ,
                     Review, MaintenanceRequest, 
                     TenantApplication,
                     Profile,PropertyImage,
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
def home(request):
    return JsonResponse({"message": "Welcome to the homepage!"})

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

        print("FILES RECEIVED:", self.request.FILES)  # Debugging output
        images = self.request.FILES.getlist("images")  # Ensure this returns a list
        print("IMAGES:", images)  # Debugging output

        if not images:
            raise serializers.ValidationError({"images": "No images received."})


        category_id = self.request.data.get("category")  # Get category from request data
        category = None
        if category_id:
            try:
                category = Category.objects.get(id=category_id)  # Fetch the category instance
            except Category.DoesNotExist:
                raise serializers.ValidationError({"category": "Invalid category ID"})

        property_instance =serializer.save(landlord=self.request.user, category=category)
        # Handle multiple images
        images = self.request.FILES.getlist('images')
        for image in images:
            # You can optionally use boto3 here
            key = f"property-images/{image}"
            upload_file_to_s3(image, settings.AWS_STORAGE_BUCKET_NAME, key)

            # Create the PropertyImage instance
            PropertyImage.objects.create(property=property_instance, image=image)
            



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
            property = Myhome.objects.get(tenant=user)
            # serializer.save(tenant=user, property=home.property)
            return MaintenanceRequest.objects.filter(tenant=user, property=property)
        return MaintenanceRequest.objects.none()  # Return an empty queryset for non-tenants

    def perform_create(self, serializer):

        user = self.request.user

        # Get the property ID from the request
        property_id = self.request.data.get('property')

        home = Property.objects.get(tenant=user, id=property_id)
        serializer.save(tenant=user, property = home)

    def get(self,request):
        user = self.request.user
        if user.role == "tenant":
            maintenance_requests = MaintenanceRequest.objects.filter(tenant=user)
            serializer = MaintenanceRequestSerializer(maintenance_requests, many=True)
            return Response(serializer.data)
       
        return Response({"message": "You do not have permission to view this data."})

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
        stripepaymentintentobject = Payment.objects.filter(stripe_payment_id=paymentConfirmation.id).first()

        if paymentConfirmation.status == "succeeded":
            
            property.is_available = False
            property.tenant = self.request.user
            
            property.save()
            Myhome.objects.create(property=property, tenant=self.request.user)
            stripepaymentintentobject.status = 'succeeded'
            stripepaymentintentobject.save()

        elif paymentConfirmation.status == "null":
            
            stripepaymentintentobject.status = 'failed'
            stripepaymentintentobject.save()

        else:
            stripepaymentintentobject.status = 'pending'
            stripepaymentintentobject.save()

        

        return Response({
            'message': 'Payment successful and property updated',
            'paymentDetails': paymentConfirmation  # Include the payment details here
            })


    
# Review View
class ReviewPostView(APIView):
    
    def post(self,request):
        name = request.user
        property_id = request.data.get("property_id")
        content = request.data.get("content")

        # Validate property
        property_instance = get_object_or_404(Property, id=property_id)

        has_lived_there = Myhome.objects.filter(tenant=name, property=property_instance).exists()

        if not has_lived_there:
            return Response({"error": "You can only review properties you have stayed in."})
   
        review = Review.objects.create(name=name,property=property_instance,content=content)
        # Serialize the review
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    
    def get(self,request):

        property_id = request.query_params.get("property_id")  # Get property_id from query params
        
        if not property_id:
            return Response({"error":"Property Id not passed"})
            

        # Get the property instance
        property_instance = get_object_or_404(Property, id=property_id)

        reviews = Review.objects.filter(property=property_instance)

        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=200)

# Payment View
class PaymentHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        tenant = request.user.id
        payments = Payment.objects.filter(tenant=tenant)
        # Serialize the payment data
        serializer = PaymentSerializer(payments,many=True)
        print(serializer.data)

        return Response(serializer.data)


class PropertyImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        property_id = request.data.get("property")
        images = request.FILES.getlist("images")

        if not property_id or not images:
            return Response({"error": "Property ID and images are required"}, status=status.HTTP_400_BAD_REQUEST)

        property_instance = Property.objects.get(id=property_id)

        for image in images:
            PropertyImage.objects.create(property=property_instance, image=image)

        return Response({"message": "Images uploaded successfully"})