from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
<<<<<<< HEAD
=======

>>>>>>> 1a2fe74802877d6e0e28ce48b891b158fc9cbf42
    path('', views.home, name='home'),
=======
    path('', views.store, name='store'),
>>>>>>> 8ac853f... Templates config
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    
]