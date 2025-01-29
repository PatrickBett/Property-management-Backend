from .views import PropertyListView, PropertyDestroyView, PropertyUpdateView, CustomUserViewSet, CustomTokenObtainPairView, MyHomeListCreateView, MyHomeRetrieveUpdateDestroyView, MyPropertyListCreateView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import create_payment_intent
router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')

urlpatterns = [
    path('api-auth/', include(router.urls)),
    path('properties/', PropertyListView.as_view(), name = 'properties'),
    path('myhome/', MyHomeListCreateView.as_view(), name = 'myhome'),
    path('myhome/<int:pk>/delete/', MyHomeListCreateView.as_view(), name = 'myhome'),
    path('properties/<int:pk>/delete/', MyHomeRetrieveUpdateDestroyView.as_view(), name = 'deletemyhome'),
    path('login/', CustomTokenObtainPairView.as_view(), name = 'login'),
    path('properties/<int:pk>/update/', PropertyUpdateView.as_view(), name = 'updateproperty'),
    path("create-payment-intent/", create_payment_intent, name="create_payment_intent"),
    path('myproperties/', MyPropertyListCreateView.as_view(), name = 'myproperties'),
]
