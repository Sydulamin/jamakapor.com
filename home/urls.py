from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
    path('', views.home, name='home'),
=======
    path('', views.store, name='store'),
>>>>>>> 8ac853f... Templates config
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    
]