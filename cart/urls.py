


from django.urls import path
from . views import add_cart

# app_name = 'cart'

urlpatterns = [
    path('add_cart/<int:id>/', add_cart, name='add_cart'),
]
