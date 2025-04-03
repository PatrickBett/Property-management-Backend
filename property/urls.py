from .views import PropertyListView, PropertyDestroyView, PropertyUpdateView, CustomUserViewSet, CustomTokenObtainPairView, MyHomeListCreateView, MyHomeRetrieveUpdateDestroyView, MyPropertyListCreateView,CustomUserListView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  (CategoryListCreateView,
                     MaintenanceRequestCreateListView, 
                     PaymentListView,
                     CreatePaymentIntentView,
                     PropertyUpdateView,FinalyzePayment,
                     ReviewPostView,PaymentHistoryView,
                     PropertyImageUploadView,
                     )
router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')

urlpatterns = [
    path('api-auth/', include(router.urls)),
    path('account/', CustomUserListView.as_view(), name = 'account'),
    path('properties/', PropertyListView.as_view(), name = 'properties'),
    path('myhome/', MyHomeListCreateView.as_view(), name = 'myhome'),
    path('myhome/<int:pk>/delete/', MyHomeListCreateView.as_view(), name = 'myhome'),
    path('properties/<int:pk>/delete/', MyHomeRetrieveUpdateDestroyView.as_view(), name = 'deletemyhome'),
    path('login/', CustomTokenObtainPairView.as_view(), name = 'login'),
    # path('properties/<int:pk>/update/', PropertyUpdateView.as_view(), name = 'updateproperty'),
    path('myproperties/', MyPropertyListCreateView.as_view(), name = 'myproperties'),
    path('maintenances/', MaintenanceRequestCreateListView.as_view(), name = 'maintenances'),
    path('categories/', CategoryListCreateView.as_view(), name = 'categories'),
    path('payments/', PaymentListView.as_view(), name = 'payments'),
    path('property/<int:pk>/update/', PropertyUpdateView.as_view(), name = 'property-update'),
    path('create-payment-intent/', CreatePaymentIntentView.as_view(), name = 'create-payment-intent'),
    path('finalyze-payment/', FinalyzePayment.as_view(), name = 'finalyze-payment'),
    path('post-review/', ReviewPostView.as_view(), name = 'reviewpost'),
    path('payment-history/', PaymentHistoryView.as_view(), name = 'payment-history'),
    path("upload-images/", PropertyImageUploadView.as_view(), name="property-image-upload"),
]
