
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from property.views import home

urlpatterns = [
    path('', home, name='root'),  # <--- this is the root `/` path
    path('admin/', admin.site.urls),
    path('api/', include('property.urls')),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)