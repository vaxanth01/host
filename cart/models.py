from django.db import models
from store.models import Product
from django.utils import timezone
from app.models import Account
# Create your models here.
from django.conf import settings
from django.db import models


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True, unique=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
        

class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE ,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now=True)
    def sub_total(self):
        return self.product.price *self.quantity

    def __str__(self):
        return f'{self.product}'
# models.py

from django.db import models
from django.conf import settings
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    USER_TYPES = [
        ('employee', 'Employee'),
        ('admin', 'Admin'),
        ('management', 'Management'),
    ]
    user_type = models.CharField(max_length=20, choices=USER_TYPES)

    def __str__(self):
        return self.user.username
    
    