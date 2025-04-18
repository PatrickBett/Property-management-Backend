from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('landlord', 'Landlord'),
        ('tenant', 'Tenant'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name



class Property(models.Model):
    landlord = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role':'landlord'},related_name='properties_as_landlord')
    tenant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role':'tenant'}, null=True , blank= True, related_name='properties_as_tenant')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class PropertyImage(models.Model):
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="property_images/", blank=True, null=True)

    def __str__(self):
        return f"Image for {self.property.title}"


class Review(models.Model):
    name = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={"role":"tenant"})
    property = models.ForeignKey(Property, on_delete= models.CASCADE)
    content =  models.TextField(max_length=1000)

    def __str__(self):
        return f'Review by {self.name} for {self.property}'


class Myhome(models.Model):
    tenant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, limit_choices_to={"role": "tenant"})#THIS ALLOWS ONE USER TO HAVE MULTIPLE HOMES
    # tenant = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True,limit_choices_to={"role": "tenant"})
    property = models.OneToOneField(Property, on_delete=models.CASCADE)

    def __str__(self):
        return f'Home for {self.tenant} at {self.property.title}'

 
class MaintenanceRequest(models.Model):

    status_choices = (
        ('submitted', 'Submitted'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    )
    
    tenant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={"role":"tenant"})
    property = models.ForeignKey(Property, on_delete= models.CASCADE)
    request = models.TextField(max_length=1000)
    status = models.CharField( max_length=20, choices=status_choices, default= 'submitted')

    def __str__(self):
        return self.request



class TenantApplication(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    tenant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={"role":"tenant"})
    property = models.ForeignKey(Property, on_delete= models.CASCADE)
    status = models.CharField(max_length=20, default="pending", choices=STATUS_CHOICES)

    def __str__(self):
        return self.status



class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE , null=True)
    profile = models.URLField(null=True, blank=True, 
        default="https://banner2.cleanpng.com/20180419/ute/avfy9wfv6.webp" )
    def __str__(self):
        return f'Profile for {self.user}'

class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="usd")
    created_at = models.DateTimeField(auto_now_add=True)
    stripe_payment_id = models.CharField(max_length=255, blank=True, null=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    tenant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=20, null=True,choices=[
        ('pending', 'Pending'),
        ('succeeded', 'Succeeded'),
        ('failed', 'Failed')
    ])
    def __str__(self):
        return f'{self.stripe_payment_id}  Amount = ${self.amount}'
    
