from helpers.billing import create_customer
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}"
    
    def save(self, *args, **kwargs):
        email = self.user.email
        if not self.strip_id:
            email = self.user.email
            if email != "" or email is not None:
                stripe_id = create_customer(email=email, raw=False)
                self.stripe_id = stripe_id
        
        super().save(*args, **kwargs)
        
