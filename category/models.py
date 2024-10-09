from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from mptt.models import MPTTModel, TreeForeignKey
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

class Category(MPTTModel):
    category_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    icon = models.CharField(max_length=200)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    
    class MPTTMeta:
        order_insertion_by = ['category_name']
    
    def __str__(self):
        return self.category_name

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])      

    class MPTTMeta:
        order_insertion_by = ['category_name']

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
