from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('store/', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment-gateway/', views.payment_gateway, name='payment_gateway'),
    path('details/', views.pro_details, name='product_details'), 
    path('success/payment/', views.success, name='success'),   
    path('fail/payment/', views.fail, name='fail'),
]