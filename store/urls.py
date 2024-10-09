from django.urls import path
from .import views

urlpatterns = [
    path('',views.store, name='store'),
    path('submit_review/<int:product_id>/',views.submit_reviews,name='submit_reviews'),
    path('edit_billing_address/', views.edit_billing_address, name='edit_billing_address'),
    path('edit_delivery_address/', views.edit_delivery_address, name='edit_delivery_address'),
    path('payment/', views.payment, name='payment'),
    path('process_payment/',views.process_payment_view, name='process_payment'),
    ]
