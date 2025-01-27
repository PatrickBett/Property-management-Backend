from django.contrib import admin
from .models import Property,CustomUser, Category, Review, MaintenanceRequest, TenantApplication

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Property)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(MaintenanceRequest)
admin.site.register(TenantApplication)
