from django.db import models
from category.models import Category
from app.models import Account
from django.urls import reverse
from django.db.models import Avg, Count
from django.template.defaultfilters import slugify

from helper import unique_product_slug_generator
from django.db.models.signals import pre_save

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.db.models import Avg, Count
from django.utils.translation import gettext_lazy as _

class DiscountType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=2000, blank=True)

    def __str__(self):
        return self.name
    

class unit_of_mesurement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=2000, blank=True)

    def __str__(self):
        return self.name
from django.db import models
from django.urls import reverse

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=2000, blank=True)
    price = models.IntegerField()
    MRP = models.IntegerField(default=0)
    image = models.ImageField(upload_to='products/photos', default="default.png")
    stock = models.IntegerField(default=0)   
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    discount_types = models.ManyToManyField(DiscountType, blank=True, related_name='products')
    weight = models.FloatField(default=0.0, help_text='Weight in kg')
    abbreviation = models.CharField(max_length=15, default='', blank=True)
    uom = models.ForeignKey(unit_of_mesurement, on_delete=models.CASCADE)  # Assuming you have a UnitOfMeasurement model
    work_choice = [
        ('P', 'Product'),
        ('S', 'Service'),
    ]
    work = models.CharField(max_length=20, choices=work_choice, default='P')
    SGST = models.IntegerField(default=0)
    CGST = models.IntegerField(default=0)
    IGST = models.IntegerField(default=0)
    CESS = models.IntegerField(default=0)
    special_cess = models.IntegerField(default=0)
    HSN_NUMBER = models.IntegerField(default=0)

    class Meta:
        ordering = ('-created_date',)

    def average_review(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def count_review(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name

    def calculate_discounted_price(self):
        """
        Calculate the discounted price based on the product price.
        """
        if self.price > 50000:
            # Apply 8% discount if the price is above ₹50,000
            discount = 0.08
        elif self.price > 10000:
            # Apply 4% discount if the price is above ₹10,000
            discount = 0.04
        elif self.price > 5000:
            # Apply 2% discount if the price is above ₹5,000
            discount = 0.02
        else:
            # No discount applied
            discount = 0

        # Calculate the discounted price
        discounted_price = self.price * (1 - discount)
        return discounted_price


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.subject
     

class ProductGalary(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image =  models.ImageField(upload_to='store/product')
  
    class Meta:
        verbose_name = 'ProductGalary'
        verbose_name_plural = 'Product Galary'
    def __str__(self):
        return self.product.product_name
    
from django.conf import settings
from django.db import models

