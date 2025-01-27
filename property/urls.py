from .views import PropertyListView, PropertyDestroyView, PropertyUpdateView, CustomUserViewSet, CustomTokenObtainPairView
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')

urlpatterns = [
    path('api-auth/', include(router.urls)),
    path('properties/', PropertyListView.as_view(), name = 'properties'),
    path('properties/<int:pk>/delete/', PropertyDestroyView.as_view(), name = 'deleteproperty'),
    path('login/', CustomTokenObtainPairView.as_view(), name = 'login'),
    path('properties/<int:pk>/update/', PropertyUpdateView.as_view(), name = 'updateproperty'),
]
