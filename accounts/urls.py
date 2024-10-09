from django.urls import path
from .import views

urlpatterns = [
    path('register/', views.register,name='register' ),
    path('login/' ,views.login,name='login' ),
    path('logout/', views.logout,name='logout' ),
    path('dashbord/', views.dashbord,name='dashbord'),
    path('my_orders/' ,views.my_orders,name='my_orders'),
    path('', views.dashbord,name='dashbord'),
    path('activate/<uidb64>/<token>/' ,views.activate,name='activate'),
    path('forgotPassword/', views.forgot_password, name='forgot-password'),
    path('resetPassword_validate/<uidb64>/<token>/', views.reset_password_validate, name='resetPassword_validate'),
    path('resetPassword/', views.reset_password, name='reset-password'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('order_detail/<int:order_id>/' ,views.order_detail, name='order_detail'),
    path('add_address', views.add_address, name='add_address'),
    path('address/', views.address, name='address'),
    path('change-password/', views.change_password, name='change_password'),
    
    ]

