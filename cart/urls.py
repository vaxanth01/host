from django.urls import path
from .import views
 

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_cart/<int:product_id>/' , views.add_cart, name='add-cart' ),
    path('remove_cart/<int:product_id>/', views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/',views.remove_cart_item, name='remove_cart_item'),
    path('update_cart_item/<int:product_id>/', views.update_cart_item, name='update_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('get_addresses/', views.get_addresses, name='get_addresses'),
    path('delete_address/', views.delete_address, name='delete_address'),
    path('set_default_address/', views.set_default_address, name='set_default_address'),
]
