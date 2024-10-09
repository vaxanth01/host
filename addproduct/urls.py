# urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('addproduct/', addProduct, name='addproduct'),
    path('addCategory/', addCategory, name='addCategory'),
    path('notification/', notification, name='notification'),
    path('addproductgallery/<int:product_id>/', addProductGallery, name='add_product_gallery'),
    path('editproduct/<int:product_id>/', editProduct, name='edit_product'), 
    path('product/<int:product_id>/delete/' ,delete_product, name='delete_product'),
    ]
